from .reusable import *
from .index import index
from .connection.login import login_, logout_
from .connection.register import register
from .profil.public.profile import profile, change_pfp, change_user_info, change_pwd, search_notfriend_user, friend_list, add_friend, delete_friend, delete_account
from .footer.termsofuse import termsofuse
from .footer.privacypolicy import privacypolicy
from .footer.legalmention import legalmention
from .footer.history import history
from .footer.team import team
from .footer.help import help
from .connection.forgottenpassword import forgotten_password
from .profil.security.passwordresetconfirm import password_reset_confirm
from .tournament.tournament import tournament
from .tournament.tournament_manager import tournament_manager, tournament_join
from .game.create_game import create_game
from .game.join_game import join_game, search_game, search_current_game
from .game.game import game, game_code
from .tournament.create_tournament import create_tournament
from .tournament.edit_tournament import edit_tournament
from .tournament.tournament_game import tournament_game
from .tournament.tournament import search_tournament, search_current_tournament, tournament_code
from .tournament.delete_tournament import delete_tournament
from .tournament.tournament_manager import tournament_player_list