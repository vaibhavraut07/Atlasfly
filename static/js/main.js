document.addEventListener("DOMContentLoaded", function () {});

function formatDate(isoDate) {
  const date = new Date(isoDate);
  const options = { year: "numeric", month: "short", day: "numeric" };
  return date.toLocaleDateString("en-US", options);
}

document.addEventListener("DOMContentLoaded", function () {
  const departDateElem = document.getElementById("depart-date");
  const arrivalDateElem = document.getElementById("arrival-date");

  departDateElem.textContent = formatDate("{{ depart_date }}");
  arrivalDateElem.textContent = formatDate("{{ arrival_date }}");

  // To diaabled past dates
  const depTimeInput = document.getElementById("Dep_Time");
  const arrivalTimeInput = document.getElementById("Arrival_Time");

  depTimeInput.addEventListener("focus", function () {
    const now = new Date();
    const minDate = now.toISOString().slice(0, 16); // Format: YYYY-MM-DDTHH:MM
    depTimeInput.min = minDate;

    // Reset the value of arrival time input when changing departure time
    arrivalTimeInput.value = "";
  });

  arrivalTimeInput.addEventListener("focus", function () {
    const depTime = new Date(depTimeInput.value);
    const minArrivalDate = new Date(depTime.getTime() + 60000); // Add one minute to departure time
    const minDate = minArrivalDate.toISOString().slice(0, 16); // Format: YYYY-MM-DDTHH:MM
    arrivalTimeInput.min = minDate;

    // Reset the value of departure time input if arrival time is before it
    const arrivalTime = new Date(arrivalTimeInput.value);
    if (arrivalTime < depTime) {
      depTimeInput.value = "";
    }
  });
});
