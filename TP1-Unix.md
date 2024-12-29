# TP1 - Being Familiar With Linux

_Sébastien Mériot_ ([@smeriot](https://twitter.com/smeriot))

Duration: 4 hours

Introduction
=====================

The different projects we are going to work on will be based upon Linux. Consequently,
being comfortable with the Linux Command-Line is a requirement before getting further.
You had probably typed few commands in the past and are not starting from zero,
neverthless this exercise is designed to make you practice and learn new things even if
you already are comfortable with `bash`.

Setup the environment
=====================

It is strongly recommended to use a Virtual Machine running a Debian or Ubuntu Linux Distribution.
You can use `VirtualBox` and run a live image to get starting.

__A Virtual Machine is strongly recommended since some network changes are going to be performed, requiring to be `root` and that could break your system.__

>Even if MacOS offers a command line as well, the commands differ from most of the Linux distribution. If you're interesting in knowing more, look at the _POSIX_ standard.

Once your environment is ready to be used, open a terminal and enjoy !

Discover Bash
=====================

As explained previously, several `Shells` are available on Linux (and Unix in general) :
- Shell Bourne (`sh`)
- Korn Shell (`ksh`)
- C Shell (`csh`)
- Zorn Shell (`zsh`)
- Bourne Again Shell (`bash`)
- Restricted Bash (`rbash`)
- And so much more.

The exercises are going to be based upon `bash` which is the most common.
The default available commands are going to be used. Some of them may be missing on minimalist distribution and may require to be installed before being used.

## File system

The easiest way to start is by using the Linux File System.

The `pwd` stands for _Print Working Directory_ and will print the directory where you currently are. When you are lucky - like when you are using a recent Linux distribution such as Ubuntu or Debian, the current working directory is displayed in your prompt. Sometimes, the symbol `~` could appear which means you are located in your _Home Directory_. `pwd` will always print the full path.

1. Which directory are you located in ?

2. Create a new directory name _TP1_ using the command `mkdir TP1` (`mkdir` stands for _Make Directory_). Use the command `ls` (standing for _List_) for list the files and folders in the current directory. Do you see the new folder ?

3. Most of the commands accept arguments (also called parameters). For instance, `ls` accepts a lot of parameter. The parameter `-l` is interesting since it display a lot more details when listing the files. What do you see when entering `ls -l` ?

4. Now create the directory _My New Directory_ and check with `ls -l`. How have you done to avoid creating 3 directories ?

5. Remove the unwanted directories using `rmdir` (_Remove Directory_). Then use the `cd` command (_Change Directory_) to get in _My New Directory_. Check with `ls` the directory is empty. Then create a new file named _Hello_ using the `touch` command. Check with `ls` the new file has been created. How big is this file ?

6. Go back in the previous directory. To do so, you can either use `cd ..` - `..` represents the parent directory - or you can also use `cd -` which means to go to the previous directory. Now, try to remove the directory _My New Directory_. What happens ?

7. Remove the file _Hello_ in the _My New Directory_ by using the `rm` command. Retry to delete the _My New Directory_ folder. Is it better ?

8. Enter the command `stat TP1`. This command will display different metadata about this directory including the last access and last modification. Which are they ?

9. Go into the _TP1_ folder and create a new empty file called _test_. Enter the command `stat .` (the `.` represent the current directory). Did the metadata changed ? You can check with the current date by entering the command `date`.

10. Create a new file named `.hello` (beggining with a `.`). Then try to list the content of the directory. Do you see this new file ? Try the command `ls -l -a` or `-ls -la`. Is it better ? Remove the 2 files.

> The file starting with a `.` are considered as hidden files on Unix. To be able to list them, you have to add the `-a` argument to the `ls` command.

## Streams

The different `bash` provide a powerful streaming system :
- `STDIN`, the standard input
- `STDOUT`, the standard output
- `STDERR`, the error output

For instance, when you are entering the command `echo "Hello World"`, the command will write in `STDOUT` the characters _Hello World_. But you can use the stream to redirect the streams elsewhere.

11. Make sure you still are in the _TP1_ folder and your folder is empty. Type the command `echo "Hello World" > hello`. Check the new file _hello_ appeared and contains 12 bytes. This command redirects `STDOUT` into the file _hello_.

12. To print the content of this new file _hello_, you can use the command `cat hello`. Confirm it does display "Hello World". Now enter the command `cat` alone, without any argument. It will wait until you type something on `STDIN` and will echo what you just typed. Use the command `cat < hello` and explain what it does.

13. If you try to enter the command `ls file`, since no file named _file_ exists, an error should be displayed on `STDERR`. To redirect the `STDERR` outputs, you can use the syntax `ls file 2> stderr` which will write in the file _stderr_ the errors. Check the file contains the very same error ?

14. Sometimes we don't want the command to output anything to avoid flooding the screen. In this case, we use the `/dev/null` file which is a kind of _void_. You can then redirect the stream to this file. Example: `cat stderr > /dev/null`. Using the previous example, how would you prevent the errors for being printed on the screen ?

15. The `/dev` directorie contains a lot of interesting files, the drives of course, but also some special files to generate _contents_. Let say we want to create a file full of zeros (in hexadecimal) to test for instance the speed of the hard drive, or the speed of an internet connection, we can use that kind of file to proceed. __We are going to do something that should never be done.__  We are going to execute a command and get ready to quickly interrupt the command by hitting CTRL+C. Enter the command `cat /dev/zeros > zeros` and hit CTRL+C quickly. List the files in the directory. How big in the file _zeros_ ?

## File content

## Environment variables 

## Variables

## Difference between " and '

Advanced Bash
=====================

Never Get Affraid Of Vi(m)
=====================

Network Tricks
=====================
