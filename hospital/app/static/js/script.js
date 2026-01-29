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


const specSelect = document.getElementById('spec_select');
const docSelect = document.getElementById('doc_select');
const procSelect = document.getElementById('proc_select');

specSelect.onchange = function() {
    const specId = specSelect.value;

    fetch('/get_doctors/' + specId).then(response => response.json()).then(data => {
        let optionHTML = '<option value="">Выберите врача</option>';
        data.forEach(d => {
            optionHTML += `<option value="${d.id}">${d.name}</option>`;
        });
        docSelect.innerHTML = optionHTML;
        procSelect.innerHTML = '<option value="">Сначала выберите врача</option>';
    });
};

docSelect.onchange = function() {
    const specId = specSelect.value;
    if (this.value) {
        fetch('/get_procedures/' + specId).then(response => response.json()).then(data => {
            let optionHTML = '';
            data.forEach(p => {
                optionHTML += `<option value="${p.id}">${p.name}</option>`;
            });
            procSelect.innerHTML = optionHTML;
        });
    }
};

});