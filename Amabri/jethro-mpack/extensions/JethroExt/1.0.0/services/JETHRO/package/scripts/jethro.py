import sys
from resource_management import *
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format

class Jethro(Script):

  def install(self, env):
    import params
    env.set_params(params)
    File(
      format("/tmp/{jethro_rpm_name}"),
      content=StaticFile(params.jethro_rpm_name)
    )
    self.install_packages(env)
    print 'Install Jethro Server'
    rpm_full_path = format("/tmp/{jethro_rpm_name}")
    Execute(
      ("rpm","-Uvh",rpm_full_path),
      sudo=True
    )


  def stop(self, env):
    import params
    env.set_params(params)
    print 'Stop the Jethro Server'
    Execute(
      ("service","jethromng", "stop"),
      user=params.jethro_user
    )

    
  def start(self, env):
    import params
    env.set_params(params)
    print 'Start the Jethro Server'
    Execute(
      ("service","jethromng", "start"),
      user=params.jethro_user
    )


  def status(self, env):
    import params
    env.set_params(params)
    print 'Status of the Jethro Server'
    Execute(
      ("service","jethromng", "status"),
      user=params.jethro_user
    )


  def configure(self, env):
    print 'Configure the Jethro Server'
    import params
    env.set_params(params)
    self.configure(env)


if __name__ == "__main__":
  Jethro().execute()