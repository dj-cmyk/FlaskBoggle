console.log('connected');

const BASE_URL = 'http://127.0.0.1:5000/';
const $startBtn = $('.start-btn');
const $guessBtn = $('#guess-btn');
const $guessTxt = $('#guess-text');
const guessed = $guessTxt.val();
const $guessMsgArea = $('.guess-messages');
const $wordsGuessed = $('.guess-history');
const $currScoreView = $('.curr-score');
const $highScoreView = $('.high-score');
const $timerDisplay = $('#timer');
const $timerSeconds = $('#timer-seconds');
const $timerBtn = $('.timer-btn');
const $guessForm = $('.guess');
const $scoredWords = $('.scored-words')
let currentScore = 0;
let highScore = 0;
const wordArray = [];
let num_games = 0;
// const $resetDisplay = $('.reset-game');
const $resetBtn = $('.reset-btn');
const $endgameDisplay = $('.endgame-display');


let seconds = 60;
$timerDisplay.hide();
$guessForm.hide();
$scoredWords.hide();
$endgameDisplay.hide();



$timerBtn.on('click', function(){
    $timerBtn.hide();
    $timerDisplay.show('slow');
    timerRun();
    $guessForm.show('slow');
    $scoredWords.show('slow');
    $guessBtn.on('click', async function(e){
        await handle_guess(e);
    })
})

function timerRun(){
    let timerSample = setInterval(function(){
        if(seconds > 0){
            $timerSeconds.text(seconds);
            seconds--;
        } else {
            $guessBtn.off()
            clearInterval(timerSample);
            $timerDisplay.hide('slow')
            $guessForm.hide('slow');
            $currScoreView.text(currentScore);
            $guessMsgArea.hide('slow');
            $endgameDisplay.show('slow');
        } 
    }, 1000)    
}


// handle guesses
async function handle_guess(e){
    e.preventDefault();
    $guessMsgArea.hide('slow');

    if(wordArray.includes($guessTxt.val())){
        $guessMsgArea.html(`<p>You already guessed ${$guessTxt.val()}</p>`)
        $guessMsgArea.show('slow');
        $guessTxt.val('');
        return 'already-guessed'
    } else {
        wordArray.push($guessTxt.val())
        const sent_word = await send_guess_to_server($guessTxt.val());
        const status_code = await get_response_from_server(sent_word);
    
        if(status_code === 'ok'){
            update_scored_words(sent_word);
            update_score(sent_word);
        } else if (status_code === 'not-on-board'){
            $guessMsgArea.html(`<p>Your guess is: ${status_code}</p>`)
            $guessMsgArea.show('slow');
        } else {
            $guessMsgArea.html(`<p>Your guess is: ${status_code}</p>`)
            $guessMsgArea.show('slow');
        }
        $guessTxt.val('');
        return status_code
    }
    
}

// send value to server using AXIOS
async function send_guess_to_server(guess){
    const response = await axios({
        method: "POST",
        url: `${BASE_URL}/guess/${guess}`,
        data: guess
      }); 
      return response.config.data;
}

async function get_response_from_server(guess){
    const res = await axios({
        method: "GET",
        url: `${BASE_URL}/guess/${guess}`,
    })

    return res.data;
}

function update_scored_words(guess){
    newLi = `<b>${guess}:</b> ${guess.length}`;
    $wordsGuessed.append(`<li class="words">${newLi}</li>`);
}

function update_score(guess){
    let word_score = guess.length
    currentScore += word_score
    $currScoreView.text(currentScore);
}

// TODO: manage end of game
// number of games played (part of requirements)


// function endGame(){
//     console.log(currentScore, highScore)
//     // num_games += 1;

//     // if(currentScore > highScore){
//     //     highScore = currentScore;
//     //     $highScoreView.text(highScore);
//     // }

//     $endgameDisplay.show('slow');
//     // $guessMsgArea.show('slow');
//     // $resetDisplay.show('slow');
//     currentScore = 0;
//     $currScoreView.text(0);
// }


// // TODO: 
