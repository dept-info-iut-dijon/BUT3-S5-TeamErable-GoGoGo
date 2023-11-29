from dataclasses import dataclass
from ...http import verify_post
from django.http import HttpRequest
from typing import Union

@dataclass
class TournamentStruct:
    name : str
    start_date : str
    end_date : str
    organisator : str
    description : str
    player_min : str
    map_size : str
    counting_method : str
    byo_yomi : str
    clock_type : str
    time_clock : str
    komi : str
    handicap : str

    @classmethod
    def verify_tournament(cls, request: HttpRequest) -> Union["TournamentStruct", Exception]:
        ret = None
        try: 
            ret = cls(
                name=verify_post(request, 'tournament-name', 'Le nom du tournoi est vide.'),
                start_date=verify_post(request, 'start-date', 'La date de début du tournoi est vide.'),
                end_date=verify_post(request, 'end-date', 'La date de fin du tournoi est vide.'),
                organisator=verify_post(request, 'tournament-organizer', 'L\'organisateur du tournoi est vide.'),
                description=verify_post(request, 'tournament-desc', 'La description du tournoi est vide.'),
                player_min=verify_post(request, 'tournament-player-min', 'Le nombre de joueurs minimum est vide.'),
                map_size=verify_post(request, 'tournament-map-size', 'Une erreur est survenue avec la taille de la carte'),
                counting_method=verify_post(request, 'tournament-counting-method', 'Une erreur est survenue avec les règles'),
                byo_yomi=verify_post(request, 'tournament-byo_yomi', 'Une erreur est survenue avec les paramètres'),
                clock_type=verify_post(request, 'tournament-clock-type', 'Une erreur est survenue avec le temps'),
                time_clock=verify_post(request, 'tournament-time-clock', 'Une erreur est survenue avec le temps'),
                komi=verify_post(request, 'tournament-komi', 'Une erreur est survenue avec le komi'),
                handicap=verify_post(request, 'tournament-handicap', 'Une erreur est survenue avec le handicap')
            )

        except Exception as e:
            ret = e
    
        return ret

    def __str__(self):
        return (f"TournamentStruct(name={self.name}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"organisator={self.organisator}, "
                f"description={self.description}, "
                f"player_min={self.player_min}, "
                f"map_size={self.map_size}, "
                f"counting_method={self.counting_method}, "
                f"byo_yomi={self.byo_yomi}, "
                f"clock_type={self.clock_type}, "
                f"time_clock={self.time_clock}, "
                f"komi={self.komi}, "
                f"handicap={self.handicap})")
