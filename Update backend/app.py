from models import add_event, get_all_events, delete_event
@app.route("/delete/<int:event_id>", methods=["POST"])
def delete(event_id):
    delete_event(event_id)
    return redirect(url_for("index"))
