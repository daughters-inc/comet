import justpy as jp
from src.ysca import YSCA
import logging

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 ' \
                 'font-semibold hover:text-white py-2 px-4 border ' \
                 'border-blue-500 hover:border-transparent rounded m-2'
input_classes = 'border m-2 p-2'
session_data = {}


def analyze_youtube_comments():
    wp = jp.WebPage()
    wp.title = "YCSA"
    wp.display_url = '/YCSA'

    form1 = jp.Form(a=wp, classes='border m-1 p-1 w-64')

    user_label = jp.Label(text='Video ID', classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in1 = jp.Input(placeholder='Video ID', a=form1, classes='form-input')
    user_label.for_component = in1
    submit_button = jp.Input(value='Submit', type='submit', a=form1, classes=button_classes)

    def submit_form(self, msg):
        msg.page.redirect = '/result'
        session_data[msg.session_id] = msg.form_data

    form1.on('submit', submit_form)

    return wp


@jp.SetRoute('/result')
def form_submitted(request):
    wp = jp.WebPage()
    wp.title = "YCSA Result"
    wp.display_url = '/result'
    video_id = session_data[request.session_id][0].value
    sentiment_analysis = YSCA(video_id)
    pretty_result = sentiment_analysis.pretty()
    result = sentiment_analysis.analyze()
    grid_options = """
    {
        defaultColDef: {
          flex: 1,
          wrapText: true,
          autoHeight: true,
          sortable: true,
          resizable: true,
        }, 
        columnDefs: [
          {headerName: "Rating", field: "rating"},
          {headerName: "Score", field: "score"},
          {headerName: "Comment", field: "comment"}
        ],
        rowData: []
    }
    """
    jp.Div(text=f"YCSA result for: https://youtu.be/{video_id}", a=wp)
    jp.Div(text='Average YCSA Rating: %.2f' % pretty_result,
           a=wp,
           classes='text-lg m-1 p-1')
    table = jp.AgGrid(a=wp,
                      options=grid_options,
                      style='height: 80vh; width: 100vw')
    for i in result:
        if i.get("error"):
            continue
        table.options.rowData.append(i)
    return wp


jp.justpy(analyze_youtube_comments)
