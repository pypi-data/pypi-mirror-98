import os

from invoke import task

from .vars import package_name


@task
def setup(c):
    c.run("docker run -d --name sonarqube -p 9000:9000 -p 9092:9092 sonarqube")


@task()
def scan(c):

    with open(
        os.path.join(package_name, "sonar-project.properties"), "w"
    ) as fp:
        fp.write(
            "sonar.projectKey={}\n"
            "sonar.python.coverage.reportPaths=coverage.xml\n"
            "sonar.scm.disabled=true".format(package_name)
        )
    scan_command = (
        "docker run -e SONAR_HOST_URL=http://172.17.0.2:9000 "
        '--user="$(id -u):$(id -g)" '
        f'-t -v "{os.getcwd()}/{package_name}:/usr/src" '
        "sonarsource/sonar-scanner-cli"
    )
    print(scan_command)
    c.run(scan_command)


@task
def kill(c):
    c.run("docker kill sonarqube")
    c.run("docker container rm sonarqube")
    c.run(f"rm -rf {package_name}/.scannerwork")
