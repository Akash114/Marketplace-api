from models import UIUpdate

def insert_ui(baner_url,video_url, q_and_a):
    new_asset = UIUpdate(
        ui_id = UIUpdate.objects.count() + 1,
        baner_url = baner_url,
        video_url = video_url,
        q_and_a = q_and_a
    )
    new_asset.save()
    return ({'id': new_asset["ui_id"]})


def get_list_ui(tansactions):
    Uicomponents = []
    for data in tansactions:
        Uicomponents.append(
            {
        "ui_id": data.ui_id,
        "baner_url":data.baner_url,
        "video_url":data.video_url,
        "q_and_a":data.q_and_a
        }
        )
    return Uicomponents


def get_all_componets():
    try:
        Uicomponents = UIUpdate.objects.all()
        data = get_list_ui(Uicomponents)
        return data
    except Exception as e:
        return str(e)


def update_ui(ui_id,baner_url,video_url, q_and_a):
    ui_component = UIUpdate.objects.filter(ui_id=ui_id)
    if(baner_url): 
        ui_component.update(baner_url=baner_url)
    if(video_url): 
        ui_component.update(baner_url=baner_url)
    if(q_and_a):  
        ui_component.update(baner_url=baner_url)
    return ui_id + "is Updated !"