let submitBtn = document.querySelector('#submitBtn')
let wordSet = new Set()
let score = []


submitBtn.addEventListener('click', handleClick)

async function handleClick(evt) {
    evt.preventDefault();
    let word = $('#word').val();
    // console.log(word)
    let response = await axios.get('/check_word', { params: { word: word } })
    // console.log(`The response from the server is: ${response.data.word} and the reversed word is ${response.data.testing}. Did we find the word? ${response.data.wordFound}`)
    let result = response.data.result
    // console.log(result)
    word_response(result, word)
    $('#word').val('');
    scoreSet(wordSet)
}
function word_response(result, word) {

    if (result === 'ok') {
        wordSet.add(word)
        $('#alert').html(`${word} has been added to the list of found words.`)
        // console.log(wordSet)
        // console.log('This word exists and is in the boggle board')

        showSet(wordSet)

    } else if (result === 'not-word') {
        $('#alert').html(`${word} does not exist`)

        // console.log('This word does not exist')
    } else {
        $('#alert').html(`${word} is not on the current board`)
    }
}

function showSet(set) {
    $('ul').empty()
    set.forEach(element => {
        if (wordSet.has(element)) {

            $('#word-list').append(`<li>${element}</li>`)
        } else {
            return
        }

    });
}

function scoreSet(set) {
    score = Array.from(set)
    newScore = score.join('').length
    // console.log(newScore.length)

    $('#score').html(newScore)


}

function countdown(seconds) {

    function tick() {
        //This script expects an element with an ID = "counter". You can change that to what ever you want. 
        let counter = document.getElementById("counter");

        seconds--;
        counter.innerHTML = seconds;
        if (seconds > 0) {
            setTimeout(tick, 1000);
        }

    }
    tick();

}
function removeSubmit() {
    setTimeout(function () {
        highScore()
        // console.log('Timer is done')
        submitBtn.removeEventListener('click', handleClick)
        submitBtn.addEventListener('click', function (evt) {
            evt.preventDefault()
        })

    }, 60000)
    //Add property disable to the form (google that). check if the disable goes on the form or on the input and add it in with jquery
}

async function highScore() {
    let score = $('#score').html()
    // console.log(`Current High Score is: ${score}`)
    res = await axios.post('/post_score', { score: score })
    // if (res.data.new_record) {
    //     console.log(`New record: ${score}`);
    // } else {
    //     console.log(`Final score: ${score}`);
    // }
}
//You can use this script with a call to onclick, onblur or any other attribute you would like to use. 
countdown(60);//where n is the number of minutes required. 
removeSubmit();

