// Course popups
const deleteCourseBtns = document.querySelectorAll(".deleteCourseBtn"); 
const courseDeleteModals = document.querySelectorAll(".courseDeleteModal");

deleteCourseBtns.forEach((btn, i) => {
  btn.addEventListener("click", (event) => {
    event.preventDefault();
    courseDeleteModals[i].classList.add("show"); // Use class to display
  });
});

function closeCoursePopup(event) {
  event.preventDefault();
  event.stopPropagation();
  event.target.closest(".courseDeleteModal").classList.remove("show");
}

// Student popups
const deleteStudentBtns = document.querySelectorAll(".deleteStudentBtn");
const studentDeleteModals = document.querySelectorAll(".studentDeleteModal");

deleteStudentBtns.forEach((btn, i) => {
  btn.addEventListener("click", (event) => {
    event.preventDefault();
    studentDeleteModals[i].classList.add("show"); // Use class to display
  });
});

function closeStudentPopup(event) {
  event.preventDefault();
  event.stopPropagation();
  event.target.closest(".studentDeleteModal").classList.remove("show");
}

// CSS class `show` toggles visibility



