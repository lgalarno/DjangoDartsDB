from django.forms import ModelForm, inlineformset_factory

from gamescoring.models import GameNumber, Participant

class ParticipantBBForm(ModelForm):
    class Meta:
        model = Participant
        exclude = ['rank']

class Participant501Form(ModelForm):
    class Meta:
        model = Participant
        exclude = ['score']

ParticipantBBFormSet = inlineformset_factory(GameNumber, Participant,
                                            form=ParticipantBBForm, extra=1)

Participant501FormSet = inlineformset_factory(GameNumber, Participant,
                                            form=Participant501Form, extra=1)