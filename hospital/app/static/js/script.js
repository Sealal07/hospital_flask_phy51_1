document.addEventListener('DOMContentLoaded', function(){
    const roleSelect = document.getElementById('role_select');
    const doctorFields = document.getElementById('doctor_fields');
    if (roleSelect && doctorFields){
        function toggleDoctorFields(){
            if (roleSelect.value === 'doctor'){
                doctorFields.style.display = 'block';
            }else {
                doctorFields.style.display = 'none';
            }
        }
        roleSelect.addEventListener('change', toggleDoctorFields);
        toggleDoctorFields();
    }
});