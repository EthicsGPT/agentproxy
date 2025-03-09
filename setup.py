#!/usr/bin/env python
from setuptools import setup
from setuptools.command.install import install
import subprocess
import sys


class PostInstallCommand(install):
    """Post-installation commands to initialize models."""
    def run(self):
        # First run the standard install
        install.run(self)
        
        # Then run the initialization script
        print("Running post-installation model initialization...")
        try:
            # Import the initialization module and run it
            from allow_agent.init_models import main
            main()
        except ImportError:
            print("Couldn't import the initialization module. Trying subprocess approach...")
            try:
                # Alternative: run the script as a subprocess
                subprocess.check_call([sys.executable, '-m', 'allow_agent.init_models'])
            except subprocess.CalledProcessError as e:
                print(f"Error initializing models: {str(e)}")


if __name__ == "__main__":
    setup(
        cmdclass={
            'install': PostInstallCommand,
        },
    ) 