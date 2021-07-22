##
## EPITECH PROJECT, 2018
## Makefile
## File description:
## Makefile
##

NAME	=	groundhog

SRC	=	groundhog.py

all:
	cp $(SRC) $(NAME)

clean:

fclean:	clean
	$(RM) $(NAME)

re:	fclean all

.PHONY: all clean fclean re
