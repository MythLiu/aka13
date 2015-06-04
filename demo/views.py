from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

# Create your views here.

def show(request):
    html = '''<object classid="clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921" codebase="http://download.videolan.org/pub/videolan/vlc/last/win32/axvlc.cab" id="vlc">
    <embed type="application/x-vlc-plugin" pluginspage="http://www.videolan.org" name="vlc" src="http://127.0.0.1:8554/1" width="720" height="410">
         <param name='volume' value='50' />
             <param name='autoplay' value='true' />
                 <param name='loop' value='false' />
                     <param name='fullscreen' value='false' />
                         <param name='controls' value='false' />
    </embed>
    </object>'''
    #return HttpResponse(html)
    return render(request, 'record_audio_demo.html')
