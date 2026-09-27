from flask import render_template,redirect, current_app as app,request,flash,url_for

from pkg import db
from pkg.models import Specialty
from pkg.models import Doctor

@app.route('/')
def landing():
    return render_template('care_landing.html')



@app.route('/login')
def login():
    return render_template('care_page.html')


@app.route('/reg')
def reg():
    return render_template('care_reg.html')


@app.route('/book')
def book():
    return render_template('book_appt.html')

@app.route('/seed')
def seed():
    specialty_names = [
        "Cardiology", "Dermatology", "Paediatrics",
        "General Medicine", "Orthopaedics",
    ]

    specialties = {}
    for name in specialty_names:
        existing = Specialty.query.filter_by(name=name).first()
        specialties[name] = existing if existing else Specialty(name=name)
        if not existing:
            db.session.add(specialties[name])

    db.session.commit()

    doctors_data = [
        ("Ade", "Bello", "ade.bello@carepoint.com", "Cardiology", "M", "LIC001"),
        ("Chiamaka", "Okoye", "chiamaka.okoye@carepoint.com", "Cardiology", "F", "LIC002"),
        ("Tunde", "Adeyemi", "tunde.adeyemi@carepoint.com", "Dermatology", "M", "LIC003"),
        ("Ngozi", "Eze", "ngozi.eze@carepoint.com", "Dermatology", "F", "LIC004"),
        ("Femi", "Ogundipe", "femi.ogundipe@carepoint.com", "Paediatrics", "M", "LIC005"),
        ("Bisi", "Fashola", "bisi.fashola@carepoint.com", "Paediatrics", "F", "LIC006"),
        ("Musa", "Ibrahim", "musa.ibrahim@carepoint.com", "General Medicine", "M", "LIC007"),
        ("Kemi", "Afolabi", "kemi.afolabi@carepoint.com", "Orthopaedics", "F", "LIC008"),
    ]

    for first, last, email, specialty_name, gender, licence_no in doctors_data:
        if not Doctor.query.filter_by(email=email).first():
            db.session.add(Doctor(
                first_name=first, last_name=last, email=email,
                specialty=specialties[specialty_name],
                gender=gender, licence_no=licence_no, availabilty=True,
            ))

    db.session.commit()
    return "Seeding complete."

@app.route('/admin')
def admin():
    specialty_id = request.args.get('specialty_id', type=int)
    search = request.args.get('search', '').strip()

    query = Doctor.query

    if specialty_id:
        query = query.filter(Doctor.specialty_id == specialty_id)

    if search:
        query = query.filter(
            db.or_(
                Doctor.first_name.ilike(f'%{search}%'),
                Doctor.last_name.ilike(f'%{search}%')
            )
        )

    # Order alphabetically by last name
    all_doctors = query.order_by(Doctor.last_name.asc()).all()

    specialties = Specialty.query.order_by(Specialty.name.asc()).all()

    return render_template(
        'care_dash_admin.html',
        doctors=all_doctors,
        specialties=specialties,
        selected_specialty=specialty_id,
        search=search
    )



@app.route('/admin/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    specialties = Specialty.query.all()

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        specialty_id = request.form.get('specialty_id')
        gender = request.form.get('gender')
        licence_no = request.form.get('licence_no')
        availability = True if request.form.get('availability') == 'on' else False

        if not all([first_name, last_name, email, specialty_id, gender, licence_no]):
            flash('Invalid information submitted.', 'error')
            return redirect(url_for('add_doctor'))

        existing = Doctor.query.filter_by(email=email).first()
        if existing:
            flash('A doctor with this email already exists.', 'error')
            return redirect(url_for('add_doctor'))

        new_doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            specialty_id=specialty_id,
            gender=gender,
            licence_no=licence_no,
            availabilty=availability,
        )
        db.session.add(new_doctor)
        db.session.commit()

        flash('Doctor created successfully.', 'success')
        return redirect(url_for('admin'))

    return render_template('doctor_form.html', specialties=specialties)


@app.route('/admin/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    specialties = Specialty.query.all()

    if not doctor:
        flash('Doctor not found.', 'error')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        specialty_id = request.form.get('specialty_id')
        gender = request.form.get('gender')
        licence_no = request.form.get('licence_no')
        availability = True if request.form.get('availability') == 'on' else False

        if not all([first_name, last_name, email, specialty_id, gender, licence_no]):
            flash('Invalid information submitted.', 'error')
            return redirect(url_for('edit_doctor', doctor_id=doctor.id))

        doctor.first_name = first_name
        doctor.last_name = last_name
        doctor.email = email
        doctor.specialty_id = specialty_id
        doctor.gender = gender
        doctor.licence_no = licence_no
        doctor.availability = availability

        db.session.commit()

        flash('Doctor updated successfully.', 'success')
        return redirect(url_for('admin'))

    return render_template('doctor_form.html', specialties=specialties, doctor=doctor)



@app.route('/admin/doctors/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        flash('Doctor not found.', 'error')
        return redirect(url_for('admin'))

    db.session.delete(doctor)
    db.session.commit()

    flash('Doctor deleted successfully.', 'success')
    return redirect(url_for('admin'))