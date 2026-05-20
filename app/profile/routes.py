from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.profile.services import get_progress_with_names, get_module_progress_summary

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def index():
    progress_items = get_progress_with_names(current_user.id)
    module_summary = get_module_progress_summary(current_user.id)
    return render_template('profile/index.html', 
                           progress_items=progress_items,
                           module_summary=module_summary, page_title='Личный кабинет')