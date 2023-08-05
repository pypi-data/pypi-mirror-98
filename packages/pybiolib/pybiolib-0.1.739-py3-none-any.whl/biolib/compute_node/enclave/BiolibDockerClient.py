import docker
import enclave_config
import tarfile
import zipfile
import logging
import os
import io
from mappings import Mappings, path_without_first_folder

class BiolibDockerClient():
    """
    An abstraction to manage and run biolib docker containers
    """

    def __init__(self):
        self.biolib_logger = logging.getLogger('biolib')
        self.docker_api_client = docker.APIClient(base_url=enclave_config.DOCKER_SOCKET_PATH)
        self.docker_client = docker.from_env()
        self.container = None
        self.container_id = None
        self.source_mappings = None
        self.input_mappings = None
        self.output_mappings = None
        self.arguments = None

    def set_mappings(self, input_mappings, source_mappings, output_mappings, arguments):
        self.input_mappings = input_mappings
        self.source_mappings = source_mappings
        self.output_mappings = output_mappings
        self.arguments = arguments

    def create_container(self, image, command, working_dir):
        self.container = self.docker_api_client.create_container(
                    image=image,
                    command=command,
                    working_dir=working_dir
        )
        self.container_id = self.container.get('Id')
    
    def run_container(self):
        self.docker_api_client.start(self.container_id)
        exit_code = self.docker_api_client.wait(self.container_id)['StatusCode']

        stdout = self.docker_api_client.logs(self.container_id, stdout=True, stderr=False)
        stderr = self.docker_api_client.logs(self.container_id, stdout=False, stderr=True)
        
        mapped_output_files = self.get_output_files()
        return stdout, stderr, exit_code, mapped_output_files

    def add_file_to_tar(self, tar, current_path, mapped_path, data):
        if current_path.endswith('/'):    
            # Remove trailing slash as tarfile.addfile appends it automatically
            tarinfo = tarfile.TarInfo(name=mapped_path[:-1])    
            tarinfo.type = tarfile.DIRTYPE
            tar.addfile(tarinfo)

        else:
            tarinfo = tarfile.TarInfo(name=mapped_path)
            file_like = io.BytesIO(data)
            tarinfo.size = len(file_like.getvalue())
            tar.addfile(tarinfo, file_like)

    def make_input_tar(self, files):
        input_tar = tarfile.open('input.tar', 'w')
        input_mappings = Mappings(self.input_mappings, self.arguments)
        for path, data in files.items():
            # Make all paths absolute
            if not path.startswith('/'):
                path = '/' + path

            mapped_file_names = input_mappings.get_mappings_for_path(path)
            for mapped_file_name in mapped_file_names:
                self.add_file_to_tar(tar=input_tar, current_path=path, mapped_path=mapped_file_name, data=data)

        input_tar.close()

    def make_runtime_tar(self, runtime_zip_data):
        runtime_tar = tarfile.open('runtime.tar', 'w')
        runtime_zip = zipfile.ZipFile(io.BytesIO(runtime_zip_data))
        source_mappings = Mappings(self.source_mappings, self.arguments)
        
        for zip_file_name in runtime_zip.namelist():
            # Make paths absolute and remove root folder from path
            file_path = '/' + path_without_first_folder(zip_file_name)
            mapped_file_names = source_mappings.get_mappings_for_path(file_path)
            for mapped_file_name in mapped_file_names:
                file_data = runtime_zip.read(zip_file_name)
                self.add_file_to_tar(tar=runtime_tar, current_path=zip_file_name, mapped_path=mapped_file_name, data=file_data)

        runtime_tar.close()

    def map_and_copy_input_files_to_container(self, files):
        self.make_input_tar(files)
        input_tar_bytes = open('input.tar', 'rb').read()
        self.docker_api_client.put_archive(self.container_id, '/', input_tar_bytes)

    def map_and_copy_runtime_files_to_container(self, runtime_zip_data):
        self.make_runtime_tar(runtime_zip_data)
        runtime_tar_bytes = open('runtime.tar', 'rb').read()
        self.docker_api_client.put_archive(self.container_id, '/', runtime_tar_bytes)

    def get_output_files(self):
        input_tar = tarfile.open('input.tar')
        input_tar_filelist = input_tar.getnames()

        if os.path.exists('runtime.tar'):
            runtime_tar = tarfile.open('runtime.tar')
            runtime_tar_filelist = runtime_tar.getnames()

        mapped_output_files = {}
        for mapping in self.output_mappings:
            try:
                tar_bytes_generator, _ = self.docker_api_client.get_archive(self.container_id, mapping['from_path'])
            except Exception as e:
                self.biolib_logger.error(e)
                continue

            tar_bytes_obj = io.BytesIO()
            for chunk in tar_bytes_generator:
                tar_bytes_obj.write(chunk)

            tar = tarfile.open(fileobj=io.BytesIO(tar_bytes_obj.getvalue()))
            for file in tar.getmembers():
                file_obj = tar.extractfile(file)

                # Skip empty dirs
                if not file_obj:
                    continue
                file_data = tar.extractfile(file).read()

                # Remove parent dir from tar file name and prepend from_path. Except if from_path is root '/', that works out of the box
                if mapping['from_path'].endswith('/') and mapping['from_path'] != '/':
                    file_name = mapping['from_path'] + path_without_first_folder(file.name)
                
                # When getting a file use the from_path as directory info (absolute path) is lost when using get_archive on files
                else:
                    file_name = mapping['from_path']

                # Filter out unchanged input files
                if file_name in input_tar_filelist and input_tar.extractfile(file_name).read() == file_data:
                    continue

                # Filter out unchanged source files if provided
                if runtime_tar and file_name in runtime_tar_filelist and runtime_tar.extractfile(file_name).read() == file_data:
                    continue

                mapped_file_names = Mappings([mapping], self.arguments).get_mappings_for_path(file_name)
                for mapped_file_name in mapped_file_names:
                    mapped_output_files[mapped_file_name] = file_data

        return mapped_output_files
