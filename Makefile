##
## EPITECH PROJECT, 2024
## ggg
## File description:
## ggg
##
all:
	cp main.py epytodolevrai
	chmod 777 epytodolevrai
clean:
	rm -rf epytodolevrai

fclean: clean

re:	all
	fclean
