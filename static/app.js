class MakeBoggle{

    constructor(boardId, seconds=60){
        this.seconds = seconds
        this.showTimer()
        this.score = 0;
        this.words = new Set ()
        this.board = $("#" + boardId)

        this.timer = setInterval(this.tick.bind(this), 1000)

        $(".submit-word",this.board).on("submit", this.submittingForm.bind(this))
    }

    addWord(word) {
        $(".accepted-words", this.board).append($("<li>", {text:word}));
    };

    showScore(){
        $(".score", this.board).text(this.score)
    }

    message(msg,cls){
        $(".message",this.board).text(msg).removeClass().addClass(`message ${cls}`)
    }

    async submittingForm(event){
        event.preventDefault()
        const $word = $(".word",this.board)
        
        let word = $word.val();

        if (!word){
            return
        };

        if (this.words.has(word)){
            this.message(`You have already submitted ${word}`, "err")
            return
        }
            
        const res = await axios.get("/word-check", 
            {params:
                {word : word}
            })

        if (res.data.result === "not-word"){
            this.message(`${word} is not a valid word`, "err")
        }
        else if (res.data.result === "not-on-board"){
            this.message(`${word} is not a word on this board`, "err")
        }
        else{
            this.addWord(word)
            this.score += word.length
            this.showScore()
            this.words.add(word);
            this.message(`${word} has been added`,"ok")
        }
        $word.val("").focus();
    }
    showTimer(){
        $(".timer",this.board).text(this.seconds)
    }

    async tick(){
        this.seconds -= 1
        this.showTimer()

        if (this.seconds === 0){
            clearInterval(this.timer)
            await this.scoreGame()
        }
    }

    async scoreGame(){
        $(".submit-word",this.board).hide()
        const res = await axios.post("/post-score", {score : this.score})
        if (res.data.brokeRecord){
            this.message(`New Record: ${this.score}`,"ok")
        }
        else{
            this.message(`Final score: ${this.score}`,"ok")
        }
    }
}



