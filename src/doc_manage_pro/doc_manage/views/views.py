from django.shortcuts import redirect
from ..items.cosine_similarity_test import cos
def index(self):
    return redirect('doc:upload') 

def cos_test(self):
    cos(self)
    return redirect('doc:upload') 