"use strict"

class SwitchingCalendar{
    constructor(body_id, label_id, left_id, right_id) {
        this.calendar_body = document.getElementById(body_id);
        this.calendar_label = document.getElementById(label_id);
        this.left_switcher = document.getElementById(left_id);
        this.right_switcher = document.getElementById(right_id);
        this.current_date = new Date();
        this.fillCalendar();
        this.left_switcher.addEventListener('click', () => {this.changeMonth(-1);});
        this.right_switcher.addEventListener('click', () => {this.changeMonth(1);});
    }

    static MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    
    static getEmptyCalCell() {
        let obj = document.createElement('div');
        obj.className = 'col-1 btn btn-warning';
        return obj;
    }

    static getActiveCalCell(day) {
        let obj = document.createElement('a');
        obj.href = './day.html';
        obj.textContent = day;
        obj.className = 'col-1 btn btn-success';
        return obj;
    }

    static getFilledCalCell(day) {
        let obj = document.createElement('a');
        obj.href = './day.html';
        obj.textContent = day;
        obj.className = 'col-1 btn btn-danger';
        return obj;
    }

    setCalLabel() {
        this.calendar_label.textContent = SwitchingCalendar.MONTHS[this.current_date.getMonth()] + ' ' + this.current_date.getFullYear();
    }

    appendCellInCalendar(cell) {
        this.calendar_body.appendChild(cell);
    }

    resetCalendar() {
        while (this.calendar_body.childNodes.length > 0) {
            this.calendar_body.removeChild(this.calendar_body.firstChild);
        }
    }

    changeMonth(delta) {
        this.current_date = new Date(this.current_date.getFullYear(), this.current_date.getMonth()+delta);
        this.fillCalendar();
    }

    fillCalendar() {
        this.resetCalendar();
        this.setCalLabel();
    
        let first_day = new Date(this.current_date.getFullYear(), this.current_date.getMonth(), 1)
        let last_day = new Date(this.current_date.getFullYear(), this.current_date.getMonth()+1, 0)
        let gaps_start = first_day.getDay() == 0 ? 6 : first_day.getDay() - 1;
        let gaps_end = last_day.getDay() == 0 ? 0 : 7 - last_day.getDay();
    
        for (let i = 0; i < gaps_start; ++i) {
            this.appendCellInCalendar(SwitchingCalendar.getEmptyCalCell());
        }
        
        for (let i = 0; i < last_day.getDate(); ++i) {
            if (Math.random() > 0.5)
                this.appendCellInCalendar(SwitchingCalendar.getActiveCalCell(i+1));
            else 
                this.appendCellInCalendar(SwitchingCalendar.getFilledCalCell(i+1));
        }
        
        for (let i = 0; i < gaps_end; ++i) {
            this.appendCellInCalendar(SwitchingCalendar.getEmptyCalCell());
        }
    }
}