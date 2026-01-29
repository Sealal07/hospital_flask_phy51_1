
const docSelect = document.getElementById('doc_select');
const datePicker = document.getElementById('date_picker');
const timeGrid = document.getElementById('time-grid');
const timeSection = document.getElementById('time-section');
const timeInput = document.getElementById('selected_time_input');

const allSlots = [];
for(let h=9; h<20; h++) {
    for(let m=0; m<60; m+=20) {
        allSlots.push(`${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`);
    }
}

function updateSlots() {
    const docId = docSelect.value;
    const date = datePicker.value;

    if (!docId || !date) {
        timeSection.style.display = 'none';
        return;
    }

    fetch(`/get_booked_slots/${docId}/${date}`)
        .then(res => res.json())
        .then(bookedSlots => {
            timeSection.style.display = 'block';
            timeGrid.innerHTML = '';
            timeInput.value = '';

            allSlots.forEach(slot => {
                const div = document.createElement('div');
                div.className = 'time-slot';
                div.textContent = slot;

                if (bookedSlots.includes(slot)) {
                    div.classList.add('booked');
                } else {
                    div.onclick = function() {
                        document.querySelectorAll('.time-slot').forEach(s => s.classList.remove('selected'));
                        div.classList.add('selected');
                        timeInput.value = slot;
                    };
                }
                timeGrid.appendChild(div);
            });
        });
}

docSelect.onchange = updateSlots;
datePicker.onchange = updateSlots;