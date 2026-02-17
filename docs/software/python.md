# Python and R with Anaconda

This tutorial is adapted from the  CU Boulder Research Computing documentation, which is also licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a>

To support diverse _Python_ and _R_ workflows, users can utilize [Anaconda](http://anaconda.com). Anaconda 
provides the _Conda_ package manager, which allows for easy installation of software and associated 
packages. The _Conda_ package manager provides support for _Python_, _R_, and many other application stacks. 
[Mamba](https://mamba.readthedocs.io/) is an alternative package manager that allows parallel downloading of repository data and package files using multi-threading.


## Configuring Conda and Mamba with `.condarc`

The Conda and Mamba package managers allow modification of default settings. These settings are specified in a text file called `.condarc`. For possible configuration options, please see [Using the .condarc conda configuration file](https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html#using-the-condarc-conda-configuration-file). The `.condarc` file should exist within a user's `/home/$USER` directory and can be quickly accessed using the file's full path at `~/.condarc`. A `.condarc` file is important because by default Conda and Mamba will put all package source code and environments in your `/home/$USER` directory. This quickly becomes an issue because your `/home/$USER` directory has limited storage capacity (see [The Home Filesystem](../compute/filesystems.md#the-home-filesystem) section). For this reason, it is highly suggested that user's redirect material to `/projects/$USER`.

````{important}
When loading the Anaconda or Mamba modules, a `.condarc` file will be created for you in your `/home/$USER` directory, if the file does not exist. If the file is created for you, it will contain the following content, which places Conda and Mamba items in your `/projects/$USER` directory:

```bash
pkgs_dirs:
  - /projects/$USER/.conda_pkgs
envs_dirs:
  - /projects/$USER/software/anaconda/envs
```
````

Although we will automatically create this file for you when you load the associated modules, you may want to modify `.condarc`. This can be done by opening your `.condarc` file in your favorite text editor (e.g., nano, vim) and modifying it.

```
[johndoe@sc3cpu-a7-u19-1 ~]$ nano ~/.condarc
```

After making changes, save and exit the file. Any modifications made and saved will be permanent unless you modify `.condarc` later.



## Using Conda:

To create your own computing environments, you can do the following:

__1. Initialize Anaconda if you haven't already done so:__
 
```
[johndoe@c3cpu-a7-u19-1 ~]$ module load anaconda
(base) [johndoe@c3cpu-a7-u19-1 ~]$ 
```

__2. Create a custom environment:__

Here we create a new environment called _mycustomenv_ (you can call it anything you want!)
```
(base) [johndoe@c3cpu-a7-u19-1 ~]$ conda create -n mycustomenv
```

If you want a specific version of python or R, you can modify the above command as follows (e.g.):  

_Python v2.7.16:_
```
(base) [johndoe@c3cpu-a7-u19-1 ~]$ conda create -n mycustomenv python==2.7.16
```

_Python v3.6.8:_
```
(base) [johndoe@c3cpu-a7-u19-1 ~]$ conda create -n mycustomenv python==3.6.8
```

_Latest version of R:_
```
(base) [johndoe@c3cpu-a7-u19-1 ~]$ conda create -n mycustomenv r-base
```

__3. Activate your new environment:__

```
(base) [johndoe@c3cpu-a7-u19-1 ~]$ conda activate mycustomenv
(mycustomenv) [johndoe@c3cpu-a7-u19-1 ~]$ 
```

If successful, your prompt will now be preceded with `(mycustomenv)`.

__4. Install needed packages in your new environment:__

The best way to do this for python packages is to install everything you 
need with one command, because it forces conda to resolve package 
conflicts. For example:

```
(mycustomenv) [johndoe@c3cpu-a7-u19-1 ~]$ conda install numpy scipy tensorflow
```

For R packages, it is easiest to start an R session and then install the 
packages as you normally would with "install.packages". For example:

```
(mycustomenv) [johndoe@c3cpu-a7-u19-1 ~]$ R
>install.packages("ggplot2")
```
If you encounter a `--- Please select a CRAN mirror for use in this session ---` message, you can select a US mirror from the provided list or use the `repos` install flag:
```
>install.packages('RMySQL', repos='http://cran.us.r-project.org')
```

For more information on managing conda environments, [check out Anaconda's documentation here.](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)


### Basic Conda commands to get you started:

| Command | Function |
|---------|----------|
| `conda list` | List the packages currently installed in the environment |
| `conda search <package>` | Searches the Anaconda package channel for a package named `<pakage>` |
| `conda install <package>` | Installs a package named `<package>` to your currently loaded environment |
| `conda uninstall <package>` | Uninstalls a package named `<package>` from your currently loaded environment |
| `conda env list` | List the Conda environments currently available |
| `conda create <env>` | Creates a new anaconda environment named `<env>` |
| `conda remove --name <env> --all` | Removes an environment named `<env>` |
| `conda deactivate` | Deactivates current environment |

### Troubleshooting

If you are having trouble loading a package, you can use `conda list` or `pip freeze` to list the available packages and their version numbers in your current Conda environment. Use `conda install <package>` to add a new package or `conda install <package==version>` for a specific version; e.g., `conda install numpy=1.16.2`.

Sometimes Conda environments can "break" if two packages in the environment require different versions of the same shared library. In these cases you try a couple of things.
* Reinstall the packages all within the same install command (e.g., `conda install <package1> <package2>`). This forces Conda to attempt to resolve shared library conflicts. 
* Create a new environment and reinstall the packages you need (preferably installing all with the same `conda install` command, rather than one-at-a-time, in order to resolve the conflicts).

## Mamba Package Manager

[Mamba](https://mamba.readthedocs.io/) is a fast, robust, and cross-platform package manager that aims to be a drop-in replacement for _Conda_. Utilizing Mamba can improve the speed and reliability of constructing an environment. 

```
module load miniforge
```

The command above activates the base environment provided by Mamba. You will know that Mamba has been correctly loaded once you see `(base)` in front of your prompt. For example: 

```
(base) [johndoe@c3cpu-a7-u19-1 ~]$
```

Once Mamba has been properly loaded, you can utilize almost all core command and configuration options available to _Conda_. For commands, this can be done by replacing `conda` with `mamba`. For example:

```
[johndoe@c3cpu-a7-u19-1 ~]$ mamba create -n mycustomenv
```

```{note}
Mamba will utilize configurations specified in `.condarc`. For more information on the `.condarc` file, see [Configuring Conda and Mamba with .condarc](#configuring-conda-and-mamba-with-condarc) above.
``` 


## Dbus Error

If you see a 'dbus' connection error when trying to connect via a virtual environment:

```
Could not connect to session bus: Failed to connect to socket /tmp/dbus-oBg2HbRfLi: Connection refused.
```
This is likely due to your `~/.bashrc` configuration file auto-activating a Conda environment with a problematic dbus package. You can resolve this issue by opening your `~/.bashrc` with a text editor (ex. vim, nano) and commenting out the following lines (or any lines that add a Conda environment to your `$PATH`):

```{tip}
Commenting lines out instead of removing them will allow you to add them back in later if needed. These lines have been commented out using `#` preceding each line.
```

```
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
# __conda_setup="$('/curc/sw/anaconda3/2019.07/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "/curc/sw/anaconda3/2019.07/etc/profile.d/conda.sh" ]; then
#         . "/curc/sw/anaconda3/2019.07/etc/profile.d/conda.sh"
#     else
#         export PATH="/curc/sw/anaconda3/2019.07/bin:$PATH"
#     fi
# fi
# unset __conda_setup
# <<< conda initialize <<<

```

Keep in mind that doing this means Conda is not automatically sourced by your `~/.bashrc` so you will have to manually source the base Conda environment with `module load anaconda` to activate the base environment.


