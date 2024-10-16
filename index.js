const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');

const quizQuestions = [
    {
        question: "Quelle est la capitale de la France? 🇫🇷",
        answers: {
            a: 'Lyon',
            b: 'Paris',
            c: 'Marseille'
        },
        correctAnswer: 'b'
    },
    {
        question: "De quoi est composé l'eau? 💧",
        answers: {
            a: 'Oxygène et azote',
            b: 'Hydrogène et oxygène',
            c: 'Hydrogène et azote'
        },
        correctAnswer: 'b'
    },
    {
        question: "Quel joueur a marqué le plus de points dans l'histoire de la NBA? 🏀",
        answers: {
            a: 'Michael Jordan',
            b: 'Kareem Abdul-Jabbar',
            c: 'LeBron James'
        },
        correctAnswer: 'b'
    },
    {
        question: "Quel est le nom de l'équipe de basket de Los Angeles? 🏆",
        answers: {
            a: 'Lakers',
            b: 'Clippers',
            c: 'Heat'
        },
        correctAnswer: 'a'
    },
    {
        question: "Qui a remporté le titre de MVP de la NBA en 2021? 🥇",
        answers: {
            a: 'Giannis Antetokounmpo',
            b: 'Nikola Jokić',
            c: 'Stephen Curry'
        },
        correctAnswer: 'b'
    },
    {
        question: "Quelle marque produit la Mustang? 🚗",
        answers: {
            a: 'Chevrolet',
            b: 'Ford',
            c: 'Dodge'
        },
        correctAnswer: 'b'
    },
    {
        question: "Quel est le constructeur automobile allemand connu pour ses voitures de luxe? 🇩🇪",
        answers: {
            a: 'Volkswagen',
            b: 'BMW',
            c: 'Toyota'
        },
        correctAnswer: 'b'
    },
    {
        question: "Quel type de moteur est généralement utilisé dans les voitures électriques? ⚡",
        answers: {
            a: 'Moteur à combustion interne',
            b: 'Moteur électrique',
            c: 'Moteur hybride'
        },
        correctAnswer: 'b'
    }
];

function buildQuiz() {
    const output = [];
    quizQuestions.forEach((currentQuestion, questionNumber) => {
        const answers = [];
        for (let letter in currentQuestion.answers) {
            answers.push(
                `<label>
                    <input type="radio" name="question${questionNumber}" value="${letter}">
                    ${letter} : ${currentQuestion.answers[letter]}
                </label>`
            );
        }
        output.push(
            `<div class="question"> ${currentQuestion.question} </div>
            <div class="answers"> ${answers.join('')} </div>`
        );
    });
    quizContainer.innerHTML = output.join('');
}

function showResults() { 
    const answerContainers = quizContainer.querySelectorAll('.answers');
    let numCorrect = 0;
    quizQuestions.forEach((currentQuestion, questionNumber) => {
        const answerContainer = answerContainers[questionNumber];
        const selector = `input[name=question${questionNumber}]:checked`;
        const userAnswer = (answerContainer.querySelector(selector) || {}).value;
        if(userAnswer === currentQuestion.correctAnswer) {
            numCorrect++;
            answerContainers[questionNumber].style.color = 'green';
        } else {
            answerContainers[questionNumber].style.color = 'red';
        }
    });
    resultsContainer.innerHTML = `${numCorrect} sur ${quizQuestions.length} réponses correctes`;
    
    // Animation d'explosion (feux d'artifice)
    if (numCorrect === quizQuestions.length) {
        fireworkAnimation();
    }
}


submitButton.addEventListener('click', showResults);
window.addEventListener('load', buildQuiz);
