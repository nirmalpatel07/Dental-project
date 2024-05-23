// Assuming you have a function to handle form submission
// Example JavaScript function to parse and format time
// function formatTime(timeString) {
//     // Create a Date object with the time string
//     const time = new Date(`1970-01-01T${timeString}`);
    
//     // Format the time as HH:MM:SS
//     const formattedTime = time.toTimeString().slice(0, 8);
    
//     return formattedTime;
// }

// // Example usage
// const originalTime = "11:30"; // Example time string
// const formattedTime = formatTime(originalTime);
// console.log(formattedTime); // Output: "11:30:00"


// // Function to check if the time format is correct
// function isValidTimeFormat(timeString) {
//     // Regular expression to match "HH:MM" format
//     const regex = /^(?:[01]\d|2[0-3]):(?:[0-5]\d)$/;

//     // Return true if the time string matches the format
//     return regex.test(timeString);
// }

// // Example usage
// const timeString = "11:30";
// const isValid = isValidTimeFormat(timeString);
// console.log(isValid); // Output: true (if the format is correct)




// function submitForm() {
//     // Get the selected time slot value
//     var selectedTime = document.getElementById("time").value;
    
//     // Assuming selectedTime is in format "HH:MM:SS - HH:MM:SS"
//     // Extract the start time (first part of the string)
//     var startTime = selectedTime.split(" - ")[0];
    
//     // Set the value of the hidden input field for the time field
//     document.getElementById("id_time").value = startTime;
    
//     // Now submit the form
//     document.getElementById("appointmentForm").submit();
// }


//------------------------------allows only 10 digit mobile number------------------------------//

// function validateForm() {
//     var form = document.getElementById("appointmentForm");
//     var sanitizedPhoneNumber = phoneInput.value.replace(/\D/g, '');
//     if (sanitizedPhoneNumber.length !== 10) {
//         phoneError.innerText = "Please enter a valid 10-digit mobile number.";
//         phoneInput.focus();
//         return false; // Prevent form submission
//     } else {
//         phoneError.innerText = "";
//     }
//     //  existing form validation logic
//     // Return true if the form is valid, and false otherwise
    

// }
function validatePhoneNumber(input) {
    var phoneNumber = input.value.replace(/\D/g, ''); // Remove non-numeric characters
    var phoneError = document.getElementById("phone-error");

    if (phoneNumber.length > 10) {
        var errorMessage = getErrorMessage(phoneError);
        if (errorMessage !== "") {
            phoneError.innerText = errorMessage;
        } else {
            // phoneError.innerText = "Please enter a valid 10-digit mobile number.";
        }
    } else {
        phoneError.innerText = ""; // Clear any previous error message
    }

    // Set the sanitized value back to the input field
    input.value = phoneNumber;
}

function getErrorMessage(errorElement) {
    var errorMessage = "";
    var errorListItems = errorElement.querySelectorAll("ul.errorlist li");
    errorListItems.forEach(function(item) {
        errorMessage += item.innerText + "\n";
    });
    return errorMessage.trim();
}

document.getElementById("appointmentForm").addEventListener("submit", function(event) {
    var phoneNumberInput = document.getElementById("phone");
    var phoneNumber = phoneNumberInput.value.replace(/\D/g, ''); // Remove non-numeric characters
    var phoneError = document.getElementById("phone-error");

    if (phoneNumber.length !== 10) {
        var errorMessage = getErrorMessage(phoneError);
        if (errorMessage !== "") {
            phoneError.innerText = errorMessage;
        } else {
            phoneError.innerText = "Please enter a valid 10-digit mobile number.";
        }
        phoneNumberInput.focus();
        event.preventDefault(); // Prevent form submission
    }
});




// function validatePhoneNumber(input) {
//     var phoneNumber = input.value;
//     var sanitizedPhoneNumber = phoneNumber.replace(/\D/g, ''); // Remove non-numeric characters
//     var phoneError = document.getElementById("phone-error");

//     if (sanitizedPhoneNumber.length !== 10) {
//         // If not exactly 10 digits, display an error message
//         phoneError.innerText = "Please enter a valid 10-digit mobile number.";
//     } else {
//         phoneError.innerText = ""; // Clear any previous error message
//     }

//     // Set the sanitized value back to the input field
//     input.value = sanitizedPhoneNumber;
// }

//----------------------------update time slots-------------------------------//


function updateTimeSlots(selectedDate) {
    // Send an AJAX request to fetch available slots for the selected date
    fetch(`/api/slots/?date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            // Log received data
            console.log('Received data:', data);

            // Check if data contains the 'slots' property
            if (data.slots && Array.isArray(data.slots)) {
                // Select the dropdown element by its ID
                var timeSelect = document.getElementById("time");

                // Clear existing options
                timeSelect.innerHTML = '';

                // Log number of slots
                console.log('Number of slots:', data.slots.length);

                // Populate dropdown with available slots
                data.slots.forEach(slot => {
                    console.log('Processing slot:', slot); // Log each slot
                    const option = document.createElement('option');
                    option.value = slot.id;
                
                    // Format the time slot with AM/PM
                    const startTime = formatTime(slot.hour, slot.minute,slot.am_pm);
                    option.text = startTime;
                
                    timeSelect.add(option);
                });
                

                // Set the default value for the time field
                if (timeSelect.options.length > 0) {
                    timeSelect.value = timeSelect.options[0].value;
                }
            } else {
                console.error('Error fetching available slots: Data format is not as expected');
            }
        })
        .catch(error => console.error('Error fetching available slots:', error));
}

function formatTime(hour, minute, am_pm) {
    // Convert hour to 12-hour format
    let formattedHour = (hour % 12) || 12;

    // Add leading zero to minute if necessary
    let formattedMinute = minute < 10 ? '0' + minute : minute;

    // Construct the formatted time string
    return `${formattedHour}:${formattedMinute} ${am_pm}`;
}



// function updateTimeSlots(selectedDate) {
//     fetch(`/api/slots/?date=${selectedDate}`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             const timeSelect = document.getElementById("time");
//             timeSelect.innerHTML = ''; // Clear existing options

//             if (data.slots && Array.isArray(data.slots)) {
//                 data.slots.forEach(slot => {
//                     const option = document.createElement('option');
//                     option.value = slot.id;
//                     option.text = `${slot.start_time} - ${slot.end_time}`;
//                     timeSelect.add(option);
//                 });
//             } else {
//                 console.error('Error fetching available slots: Data format is not as expected');
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching available slots:', error);
//             alert('Error fetching available slots. Please try again later.');
//         });
// }

// function updateTimeSlots(selectedDate) {
//     // Send an AJAX request to fetch available slots for the selected date
//     fetch(`/api/slots/?date=${selectedDate}`)
//         .then(response => response.json())
//         .then(data => {
//             // Log received data
//             console.log('Received data:', data);

//             // Check if data contains the 'slots' property
//             if (data.slots && Array.isArray(data.slots)) {
//                 // Select the dropdown element by its ID
//                 var timeSelect = document.getElementById("time");

//                 // Clear existing options
//                 timeSelect.innerHTML = '';

//                 // Log number of slots
//                 console.log('Number of slots:', data.slots.length);

//                 // Populate dropdown with available slots
//                 data.slots.forEach(slot => {
//                     console.log('Processing slot:', slot); // Log each slot
//                     const option = document.createElement('option');
//                     option.value = slot.id;
//                     option.text = `${slot.start_time} `;  //- ${slot.end_time}
//                     timeSelect.add(option);
//                 });

//                                 // Set the default value for the time field
//                 if (timeSelect.options.length > 0) {
//                     timeSelect.value = timeSelect.options[0].value;
//                 //    const defaultTime = timeSelect.options[0].text.split(' - ')[0]; // Extract start time from option text
//                 //     timeSelect.value = defaultTime; // Set the default value to the start time
//                   }




//                 // Set the default value for the time field
//                 // if (timeSelect.options.length > 0) {
//                 //     timeSelect.value = timeSelect.options[0].value;
//                 // }
//             } else {
//                 console.error('Error fetching available slots: Data format is not as expected');
//             }
//         })
//         .catch(error => console.error('Error fetching available slots:', error));
// }



// function updateTimeSlots(selectedDate) {
//     // Send an AJAX request to fetch available slots for the selected date
//     fetch(`/api/slots/?date=${selectedDate}`)
//         .then(response => response.json())
//         .then(data => {
//             // Log received data
//             console.log('Received data:', data);

//             // Check if data contains the 'slots' property
//             if (data.slots && Array.isArray(data.slots)) {
//                 // Select the dropdown element by its ID
//                 var timeSelect = document.getElementById("time");

//                 // Clear existing options
//                 timeSelect.innerHTML = '';

//                 // Log number of slots
//                 console.log('Number of slots:', data.slots.length);

//                 // Populate dropdown with available slots
//                 data.slots.forEach(slot => {
//                     console.log('Processing slot:', slot); // Log each slot
//                     const option = document.createElement('option');
//                     option.value = slot.id;
//                     option.text = `${slot.start_time} - ${slot.end_time}`;
//                     timeSelect.add(option);
//                 });
//             } else {
//                 console.error('Error fetching available slots: Data format is not as expected');
//             }
//         })
//         .catch(error => console.error('Error fetching available slots:', error));
// }




// function updateTimeSlots(selectedDate) {
//     // Clear existing options
//     timeSelect.innerHTML = '';

//     // Example: Adding time slots for every hour within working hours and future times
//     var startTime = new Date(selectedDate + 'T10:00:00'); // Start from 10:00 AM

//     // Loop until reaching the end of working hours or 9pm
//     while (startTime.getHours() < 21) {
//         var option = document.createElement('option');
//         option.value = startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
//         option.text = startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
//         timeSelect.add(option);
        
//         // Increment time by 1 hour
//         startTime.setHours(startTime.getHours() + 1);
//     }

//     // If no slots are available, add a default option with red text
//     if (timeSelect.options.length === 0) {
//         var defaultOption = document.createElement('option');
//         defaultOption.value = '';
//         defaultOption.text = 'No slots available';
//         timeSelect.add(defaultOption);
//     }
// }













 // Function to update time slots based on the selected date
// Clear existing options
// var timeSelect = document.getElementById('time');
// function updateTimeSlots(selectedDate) {
//     timeSelect.innerHTML = '';

//     // Example: Add 11:00 AM time slot
//     var option = document.createElement('option');
//     option.value = '11:00 AM';
//     option.text = '11:00 AM';
//     timeSelect.add(option);
// }





// function updateTimeSlots(selectedDate) {
//     // Clear existing options
//     timeSelect.innerHTML = '';

//     // Current date and time
//     var currentDateTime = new Date();

//     // Selected date
//     var selectedDateTime = new Date(selectedDate);

//     // Set working hours (10am to 1pm and 5pm to 9pm)
//     var workingHoursStart1 = new Date(selectedDate + 'T10:00:00');
//     var workingHoursEnd1 = new Date(selectedDate + 'T13:00:00');
//     var workingHoursStart2 = new Date(selectedDate + 'T17:00:00');
//     var workingHoursEnd2 = new Date(selectedDate + 'T20:30:00');

//     // Check if the selected date is today and if it's within working hours
//     if (
//         (selectedDateTime.getDate() === currentDateTime.getDate()) &&
//         ((currentDateTime >= workingHoursStart1 && currentDateTime < workingHoursEnd1) ||
//         (currentDateTime >= workingHoursStart2 && currentDateTime < workingHoursEnd2))
//     ) {
//         // If it's today and within working hours, adjust the starting time
//         var startTime = (currentDateTime <= workingHoursStart1) ? workingHoursStart1 : workingHoursStart2;
//     } else {
//         // If it's not today or outside working hours, start from the beginning of the working hours
//         var startTime = workingHoursStart1 < currentDateTime ? workingHoursStart2 : workingHoursStart1;
//     }

//     // Example: Adding time slots for every 30 minutes within working hours and future times
//     startTime.setSeconds(0);
//     startTime.setMilliseconds(0);

//     var slotsAvailable = false;

//     // Loop until reaching the end of working hours or 9pm
//     while (startTime < workingHoursEnd2 && startTime.getHours() < 21) {
//         // Check if the current time is between 1 pm and 5 pm and skip generating slots during that time
//         if (
//             (startTime >= workingHoursEnd1 && startTime < workingHoursStart2)
//         ) {
//             // Skip this time period
//             startTime = workingHoursStart2;
//         }

//         // Compare with current time to ensure future times only
//         if (startTime > currentDateTime) {
//             var endTime = new Date(startTime);
//             endTime.setMinutes(endTime.getMinutes() + 30);
//             var option = document.createElement('option');
//             option.value = startTime.toISOString().substr(11, 5) + '-' + endTime.toISOString().substr(11, 5); // Extract HH:mm from ISO string
//             option.text = startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' to ' + endTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
//             timeSelect.add(option);
//             slotsAvailable = true;
//         }

//         // Increment time by 30 minutes
//         startTime.setMinutes(startTime.getMinutes() + 30);

//         // Add 15 minutes gap if the next slot is within working hours
//         if (
//             (startTime >= workingHoursStart1 && startTime < workingHoursEnd1) ||
//             (startTime >= workingHoursStart2 && startTime < workingHoursEnd2)
//         ) {
//             startTime.setMinutes(startTime.getMinutes() + 15);
//         }
//     }

//     // If no slots are available, add a default option with red text
//     if (!slotsAvailable) {
//         var defaultOption = document.createElement('option');
//         defaultOption.value = ' ';
//         defaultOption.text = 'No slots available';
//         timeSelect.add(defaultOption);
//     }
// }



// ------------------can not select previous dates------------------//
document.getElementById('date').min = new Date().toISOString().split('T')[0]; // for minimus date 



