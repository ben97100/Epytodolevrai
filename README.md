Hello, everyone.
README consist to help you for run command in the terminal, for project "Epytodolevrai".
1. Verify environment
   sudo apt install python3
   python3 --version
2. Install librairies
   sudo apt install python3-crud.
3. Run command:
   $ python3 main.py get <res> <id>
   $ python3 main.py del <res> <id>
   $ python3 main.py add <res> <field1> <field2> ...
   $ python3 main.py update <res> <id> <field1> <field2> ...
   (without $)
4. Launch http server
   $ python3 server.py


BONUS:
If you want to make unit test, you must make that:
1. Install librairies
   sudo apt install python3-pytest -> this command equal unit test in c but it's for python language
   sudo apt install python3-mock -> this command allows to make utils.py in unit test
2. Run command
   $ pytest your_test_file_in_py
   (without $)

If you want to make e2e test, you shoud make that
1. Run command
   $ pytest e2e_test_file.py
   
