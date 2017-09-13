import sys
from resource_management import *
from resource_management.core.resources.system import File, Execute
from resource_management.libraries.functions.format import format

class JethroMng(Script):

  def install(self, env):
    import params
    env.set_params(params)
    File(
      format("/tmp/{jethromng_rpm_name}"),
      content=StaticFile(params.jethromng_rpm_name)
    )
    self.install_packages(env)
    print 'Install Jethro Manager'
    rpm_full_path = format("/tmp/{jethromng_rpm_name}")
    Execute(
      ("rpm","-Uvh",rpm_full_path),
      sudo=True
    )


  def stop(self, env):
    import params
    env.set_params(params)
    print 'Stop the Jethro Manager'
    Execute(
      ("service","jethromng", "stop"),
      user=params.jethro_user
    )

    
  def start(self, env):
    import params
    env.set_params(params)
    print 'Start the Jethro Manager'
    Execute(
      ("service","jethromng", "start"),
      user=params.jethro_user
    )


  def status(self, env):
    import params
    env.set_params(params)
    print 'Status of the Jethro Manager'
    Execute(
      ("service","jethromng", "status"),
      user=params.jethro_user
    )


  def configure(self, env):
    print 'Configure the Jethro Manager'
    import params
    env.set_params(params)
    self.configure(env)


if __name__ == "__main__":
  JethroMng().execute()