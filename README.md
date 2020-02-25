# sublime-java
A plugin for Sublime Text 3 that allows you to easily run complicated java projects


To install this plugin, simply clone the repository to a plugins directory for Sublime Text (Such as %appdata%\Sublime Text 3\Packages)

This plugin was created hastily in an attempt to make compiling java programs easier for my CS2 class, do not expect it to be a fully featured IDE for java, nor expect it to be bug free. It's terrible, has glitches, and a lot of problems. It was designed specifically to fit my needs, and not to be a releasable project, but I'm releasing it anyways! Sorry!

## Usage:

There are a few useful features of sublime-java that allow you to easily run java projects
These features are accessed through a few files that you must create in your project root directory

### java.txt:

  Contains several different options for the build system
  Each option should be on it's own line with the following syntax:
  varaiable=text
  No spaces, no quotes, and no need to escape any special characters in the text portion, the plugin does this automatically
  All of these options, including the java.txt file itself, are optional, and can be included in any order.
  
 ####  Available options:
  

    runClass:
	    The main program class to pass to the java command line program at runtime
 
    additional-options:
        Additional options to pass to the compiler at compile time
        
    run-options:
        Additional options to pass to the java command line program at runtime
        
    module-path:
        Modules to pass to the --module-path option at runtime.
        
    add-modules:
        Modules to pass to the --add-modules= option at runtime
    program-args:
        Args to pass to the java command line program at runtime. Appended after the runClass.

  
### classpath.txt:
  Contains a list of classpaths to pass to the compiler and the command line
  Each classpath to search is on it's own line, and must be the full canonical path
  Directories /bin, /src, and /. are automatically included (Relative to the project root)
  These paths do not need to be in quotes or escaped, the plugin does this automatically
  
## Keyboard shortcuts and macros

This plugin also includes several keyboard short cuts that I found useful when creating java programs:
  

    ctrl+alt+shift+n - Create a new class. Overwrites all content in the currently open file
    alt+shift+p - Add a system.out.println() at the cursor position
    alt+shift+m - Add a psvm statement at the cursor postion

  
These shortcuts are also accessible through the right-click context menu

## Required folder structure
In order to allow the plugin to work correctly, and to keep code organized, the file structure for your project must be as follows

    Project Root
    │    ├bin
    │    	This is the compiler output directory, this should be added to your .gitignore file to avoid committing binary files to a repository.
    │    ├src
    │		Put your project code here
    ├java.txt
    ├classpath.txt

## Included example
There is an example project that builds using the plugin under the example folder.
This program requires JavaFX to be installed under Windows at C:\Program Files (x86)\Java\javafx-sdk-11.0.2
