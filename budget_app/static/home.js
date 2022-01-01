

let slideImage = document.querySelectorAll(".slide-image");
let slidescontainer = document.querySelector(".slides-container");
let next_btn = document.querySelector(".next-btn")
let prev_btn = document.querySelector(".prev-btn")
let nav_dots = document.querySelector(".navigation-dots");
let single_dot = document.querySelectorAll(".single-dot")
let slideWidth = slideImage[0].clientWidth;
let currentslide = 0
// Set up the slider
function init(){
    /* 
        slideImage[0] = 0
        slideImage[1] = 100%
        slideImage[2] = 200%
        ......
    */

    slideImage.forEach((img, i) => {
        img.style.left = i*100 + "%";
    });

    slideImage[0].classList.add('active');
    create_nav_dots();
}

init();


function create_nav_dots(){
    for(i=0;i<slideImage.length;i++){
        let dot = document.createElement("div");
        dot.classList.add("single-dot")
        nav_dots.appendChild(dot);
    }
    nav_dots.children[0].classList.add('active');
}


// Next slide in carousel
next_btn.addEventListener('click', ()=>{
    if (currentslide>=slideImage.length-1){
        goToSlide(0)
        // setNavDotsActive(0);
        return 
    }
    currentslide++;
    goToSlide(currentslide);
    // setNavDotsActive(currentslide);
});

// Previous Slide
prev_btn.addEventListener('click', ()=>{
    if (currentslide<=0){
        goToSlide(slideImage.length-1)
        // setNavDotsActive(slideImage.length-1);
        return 
    }
    currentslide--;
    goToSlide(currentslide);
    // setNavDotsActive(currentslide);
});

// GoTo slide
function goToSlide(slideNumber){
    slidescontainer.style.transform = "translateX(-"+slideWidth * slideNumber+"px)";
    currentslide = slideNumber
    setActiveClass(currentslide)
}


// Set Active Class
function setActiveClass(slideNumber){
    let currentActive = document.querySelector(".slide-image.active")
    currentActive.classList.remove("active");
    slideImage[slideNumber].classList.add("active")
    setNavDotsActive(slideNumber);
}


// Set active class for navigation dots
function setNavDotsActive(slideNumber){
    console.log(nav_dots.length);
    let currentActiveDot = document.querySelector(".single-dot.active");

    currentActiveDot.classList.remove("active");
    nav_dots.children[slideNumber].classList.add("active");
}


// Budget Carousel

let budgetImage = document.querySelectorAll(".budget-image");
let budgetcontainer = document.querySelector(".budget-container");
let next_budget_btn = document.querySelector(".next-budget-btn")
let prev_budget_btn = document.querySelector(".prev-budget-btn")
let nav_budget_dots = document.querySelector(".budget-navigation-dots");
let budget_single_dot = document.querySelectorAll(" .budget-single-dot")
let budgetSlideWidth = budgetImage[0].clientWidth;
let currentBudgetSlide = 0
// Set up the slider
function budget_init(){
    /* 
        slideImage[0] = 0
        slideImage[1] = 100%
        slideImage[2] = 200%
        ......
    */

    budgetImage.forEach((img, i) => {
        img.style.left = i*150-i + "%";
    });

    budgetImage[0].classList.add('active');
    create_budget_nav_dots();
}

budget_init();


function create_budget_nav_dots(){
    for(i=0;i<budgetImage.length;i++){
        let dot = document.createElement("div");
        dot.classList.add("budget-single-dot")
        nav_budget_dots.appendChild(dot);
    }
    nav_budget_dots.children[0].classList.add('active');
}


// Next slide in carousel
next_budget_btn.addEventListener('click', ()=>{
    if (currentBudgetSlide>=budgetImage.length-1){
        goToBudgetSlide(0)
        return 
    }
    currentBudgetSlide++;
    goToBudgetSlide(currentBudgetSlide);
});

// Previous Slide
prev_budget_btn.addEventListener('click', ()=>{
    if (currentBudgetSlide<=0){
        goToBudgetSlide(budgetImage.length-1)
        return 
    }
    currentBudgetSlide--;
    goToBudgetSlide(currentBudgetSlide);
});

// GoTo slide
function goToBudgetSlide(slideNumber){
    budgetcontainer.style.transform = "translateX(-"+slideWidth * slideNumber+"px)";
    currentBudgetSlide = slideNumber
    setBudgetActiveClass(currentBudgetSlide)
}


// Set Active Class
function setBudgetActiveClass(slideNumber){
    let currentActive = document.querySelector(".budget-image.active")
    currentActive.classList.remove("active");
    budgetImage[slideNumber].classList.add("active")
    setBudgetNavDotsActive(slideNumber);
}


// Set active class for navigation dots
function setBudgetNavDotsActive(slideNumber){
    let currentActiveDot = document.querySelector(".budget-single-dot.active");

    currentActiveDot.classList.remove("active");
    nav_budget_dots.children[slideNumber].classList.add("active");
}


document.getElementById('add-cat').addEventListener('click',function (){
    let cat_input = document.getElementById("hidden-card")
    cat_input.classList.remove("hide")
    cat_input.classList.add("show")
    let input = document.querySelector("#hidden-card input")
    input.disabled = false;
});
