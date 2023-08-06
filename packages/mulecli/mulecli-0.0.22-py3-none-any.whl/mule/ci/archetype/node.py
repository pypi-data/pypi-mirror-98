from mule.ci.archetype import IArchetype
from mule.ci import config
from mule.util import npm_util, docker_util, aws_util, helm_util


class Npm(IArchetype):

    def deps(self):
        aws_util.deps()
        helm_util.deps()
        docker_util.deps()
        npm_util.deps()

    def build(self):
        version = npm_util.get_version()
        docker_util.build([f"{self.application_name}:{version}"])

    def publish(self, environment):
        version = npm_util.get_version()
        repository = aws_util.ensure_repository(self.application_name, environment)

        aws_util.ecr_login()
        repository_uri = repository['repositoryUri']
        source_image = f"{self.application_name}:{version}"
        docker_util.tag(source_image, f"{repository_uri}:{version}")
        docker_util.tag(source_image, f"{repository_uri}:latest")

        docker_util.push([
            f"{repository_uri}:{version}",
            f"{repository_uri}:latest",
        ])

    def deploy(self, environment: str):
        version = npm_util.get_version()
        if config.EKS_CLUSTER_NAME:
            aws_util.update_kubeconfig(config.EKS_CLUSTER_NAME)
        chart_path = helm_util.get_packaged_chart('rest-api')
        helm_util.deploy(self.application_name, environment, version, chart_path)

    def undeploy(self, environment: str):
        version = npm_util.get_version()
        if config.EKS_CLUSTER_NAME:
            aws_util.update_kubeconfig(config.EKS_CLUSTER_NAME)
        chart_path = helm_util.get_packaged_chart('rest-api')
        helm_util.delete(self.application_name, environment, version, chart_path)
