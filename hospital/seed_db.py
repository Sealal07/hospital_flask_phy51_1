from datetime import datetime, timedelta
from app.extensions import db
from app import create_app
from app.models import User, Doctor, Patient, Appointment, Specialization, Procedure


def seed_data():

    app = create_app()

    with app.app_context():
        print("Заполнение специализаций...")
        specs = [
            Specialization(name="Терапевт"),
            Specialization(name="Стоматолог"),
            Specialization(name="Невролог"),
            Specialization(name="Офтальмолог"),
            Specialization(name="Кардиолог")
        ]
        db.session.add_all(specs)
        db.session.commit()

        print("Заполнение процедур...")
        procs = [
            Procedure(name="Общий осмотр", specialization_id=specs[0].id),
            Procedure(name="Вакцинация", specialization_id=specs[0].id),
            Procedure(name="Чистка зубов", specialization_id=specs[1].id),
            Procedure(name="Пломбирование", specialization_id=specs[1].id),
            Procedure(name="МРТ диагностика", specialization_id=specs[2].id),
            Procedure(name="Проверка зрения", specialization_id=specs[3].id),
            Procedure(name="Подбор очков", specialization_id=specs[3].id),
            Procedure(name="ЭКГ", specialization_id=specs[4].id),
            Procedure(name="УЗИ сердца", specialization_id=specs[4].id),
            Procedure(name="Консультация по анализам", specialization_id=specs[0].id)
        ]
        db.session.add_all(procs)
        db.session.commit()

        print("Создание пользователей и врачей...")
        for i in range(1, 11):
            u_doc = User(
                username=f"doctor{i}",
                password="password123",
                email=f"doctor{i}@clinic.ru",
                role="doctor"
            )
            db.session.add(u_doc)
            db.session.flush()

            doc = Doctor(
                name=f"Доктор Специалист {i}",
                user_id=u_doc.id,
                specialization_id=specs[i % 5].id
            )
            db.session.add(doc)

        print("Создание пользователей и пациентов...")
        for i in range(1, 11):
            u_pat = User(
                username=f"patient{i}",
                password="password123",
                email=f"patient{i}@mail.ru",
                role="patient"
            )
            db.session.add(u_pat)
            db.session.flush()

            pat = Patient(
                name=f"Иванов Пациент {i}",
                user_id=u_pat.id
            )
            db.session.add(pat)

        db.session.commit()

        print("Создание записей на прием...")
        all_docs = Doctor.query.all()
        all_pats = Patient.query.all()
        all_procs = Procedure.query.all()

        for i in range(10):
            apt = Appointment(
                patient_id=all_pats[i].id,
                doctor_id=all_docs[i].id,
                procedure_id=all_procs[i].id,
                appointment_time=datetime.now() + timedelta(days=i, hours=i),
                status="scheduled"
            )
            db.session.add(apt)

        db.session.commit()
        print("База данных успешно заполнена!")


if __name__ == "__main__":
    seed_data()