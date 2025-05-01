from flask import (
    Blueprint, render_template,
    request, redirect, url_for, flash
)

main_bp = Blueprint(
    'main', __name__,
    template_folder='templates'
)

def generate_eticket(name):
    """Generate an E-Ticket number by merging the original name with INFOTC4320"""
    base = "INFOTC4320"
    eticket = []
    
    # Merge the names
    for i in range(max(len(name), len(base))):
        if i < len(name):
            eticket.append(name[i]) 
        if i < len(base):
            eticket.append(base[i])
    
    return ''.join(eticket)

# Makes generate_eticket function available to all templates in this blueprint
@main_bp.app_context_processor
def inject_eticket_generator():
    return {'generate_eticket': generate_eticket}

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/', methods=['POST'])
def index_post():
    choice = request.form.get('action')
    if choice == 'reserve':
        return redirect(url_for('main.reserve'))
    elif choice == 'admin':
        return redirect(url_for('admin.login'))
    flash('Please select a valid option.')
    return redirect(url_for('main.index'))

@main_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        if not first_name or not last_name:
            flash('Both first and last names are required', 'error')
            return redirect(url_for('main.reserve'))
        
        return render_template('reserve.html',
                            first_name=first_name,
                            last_name=last_name)
    
    return render_template('reserve.html')