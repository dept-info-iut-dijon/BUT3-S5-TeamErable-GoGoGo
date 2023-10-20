from .reusable import *
from .index import index
from .login import login_, logout_
from .register import register
from .profile import profile, change_pfp, change_user_info, change_pwd, search_notfriend_user, friend_list, add_friend, delete_friend, delete_account
from .termsofuse import termsofuse
from .privacypolicy import privacypolicy
from .legalmention import legalmention
from .history import history
from .team import team
from .help import help
from .forgottenpassword import forgotten_password
from .passwordresetconfirm import password_reset_confirm
from .tournament.tournament import tournament
from .tournament.tournament_manager import tournament_manager, tournament_join
from .create_game import create_game
from .join_game import join_game, search_game, search_current_game
from .game import game, game_code
from .tournament.create_tournament import create_tournament
from .tournament.tournament_game import tournament_game
from .tournament.tournament import search_tournament, search_current_tournament, tournament_code
from .tournament.delete_tournament import delete_tournament