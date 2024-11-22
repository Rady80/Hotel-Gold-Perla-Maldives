// Modul AngularJS a hlavní controller
angular
    .module('app', ['flexcalendar', 'pascalprecht.translate']) // Registrace modulu a závislostí
    .controller('MainController', ['$scope', function ($scope) {
        // Nastavení kalendáře
        $scope.options = {
            defaultDate: "2020-01-01", // Výchozí datum
            minDate: "2020-01-01",     // Minimální datum
            maxDate: "2045-12-31",     // Maximální datum
            disabledDates: [           // Data, která mají být zakázána
                "2015-06-22",
                "2015-07-27",
                "2015-08-13",
                "2015-08-15"
            ],
            dayNamesLength: 1,         // Zkrácené názvy dní (1: "M", 2: "Mo", 3: "Mon")
            mondayIsFirstDay: true,    // Nastavení pondělí jako prvního dne týdne
            eventClick: function (date) {
                console.log("Kliknuto na událost: ", date);
            },
            dateClick: function (date) {
                console.log("Kliknuto na datum: ", date);
            },
            changeMonth: function (month, year) {
                console.log("Změněn měsíc: ", month, "Rok: ", year);
            },
        };

        // Události v kalendáři
        $scope.events = [
            {
                description: 'Nějaká událost',
                date: "2015-08-18"
            },
            {
                description: 'Další událost',
                date: "2015-08-20"
            }
        ];
    }]);

// Definice direktivy pro kalendář
!function () {
    "use strict";

    function calendarDirective() {
        const template = `
            <div class="flex-calendar">
                <div class="month">
                    <div class="arrow {{arrowPrevClass}}" ng-click="prevMonth()"></div>
                    <div class="label">{{ selectedMonth | translate }} {{selectedYear}}</div>
                    <div class="arrow {{arrowNextClass}}" ng-click="nextMonth()"></div>
                </div>
                <div class="week">
                    <div class="day" ng-repeat="day in weekDays(options.dayNamesLength) track by $index">{{ day }}</div>
                </div>
                <div class="days" ng-repeat="week in weeks">
                    <div class="day"
                         ng-repeat="day in week track by $index"
                         ng-class="{
                             selected: isDefaultDate(day),
                             event: day.event[0],
                             disabled: day.disabled,
                             out: !day
                         }"
                         ng-click="onClick(day, $index, $event)">
                        <div class="number">{{day.day}}</div>
                    </div>
                </div>
            </div>
        `;

        return {
            restrict: "E", // Direktiva pouze jako element
            scope: {
                options: "=?", // Možnost předání vlastních parametrů
                events: "=?",  // Seznam událostí
            },
            template: template,
            controller: calendarController
        };
    }

    // Kontroler pro kalendář
    function calendarController($scope, $filter) {
        const MONTHS = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen", "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"];
        const DAYS = ["Neděle", "Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota"];

        // Nastavení dnů týdne
        $scope.weekDays = (length) => {
            const days = $scope.options.mondayIsFirstDay ? [...DAYS.slice(1), DAYS[0]] : DAYS;
            return days.map(day => day.slice(0, length));
        };

        // Kontrola, zda je datum výchozí
        $scope.isDefaultDate = (day) => {
            if (!day) return false;
            const defaultDate = new Date($scope.options.defaultDate);
            return day.year === defaultDate.getFullYear() &&
                day.month === defaultDate.getMonth() &&
                day.day === defaultDate.getDate();
        };

        // Přechod na předchozí měsíc
        $scope.prevMonth = () => {
            if ($scope.allowedPrevMonth()) {
                const currentMonth = MONTHS.indexOf($scope.selectedMonth);
                if (currentMonth === 0) {
                    $scope.selectedMonth = MONTHS[11];
                    $scope.selectedYear -= 1;
                } else {
                    $scope.selectedMonth = MONTHS[currentMonth - 1];
                }
                buildCalendar();
            }
        };

        // Přechod na další měsíc
        $scope.nextMonth = () => {
            if ($scope.allowedNextMonth()) {
                const currentMonth = MONTHS.indexOf($scope.selectedMonth);
                if (currentMonth === 11) {
                    $scope.selectedMonth = MONTHS[0];
                    $scope.selectedYear += 1;
                } else {
                    $scope.selectedMonth = MONTHS[currentMonth + 1];
                }
                buildCalendar();
            }
        };

        // Sestavení kalendáře
        function buildCalendar() {
            const monthIndex = MONTHS.indexOf($scope.selectedMonth);
            const firstDay = new Date($scope.selectedYear, monthIndex, 1).getDay();
            const totalDays = new Date($scope.selectedYear, monthIndex + 1, 0).getDate();

            $scope.weeks = [];
            let week = new Array(7).fill(null);

            for (let day = 1; day <= totalDays; day++) {
                const date = new Date($scope.selectedYear, monthIndex, day);
                const dayIndex = ($scope.options.mondayIsFirstDay ? (date.getDay() + 6) % 7 : date.getDay());

                week[dayIndex] = {
                    year: date.getFullYear(),
                    month: date.getMonth(),
                    day: day,
                    date: date,
                    disabled: isDisabledDate(date),
                    event: getEvents(date),
                };

                if (dayIndex === 6 || day === totalDays) {
                    $scope.weeks.push(week);
                    week = new Array(7).fill(null);
                }
            }
        }

        // Kontrola zakázaných dat
        function isDisabledDate(date) {
            const minDate = $scope.options.minDate ? new Date($scope.options.minDate) : null;
            const maxDate = $scope.options.maxDate ? new Date($scope.options.maxDate) : null;
            return (minDate && date < minDate) || (maxDate && date > maxDate);
        }

        // Načtení událostí
        function getEvents(date) {
            return ($scope.events || []).filter(event =>
                new Date(event.date).toDateString() === date.toDateString()
            );
        }

        // Inicializace
        $scope.selectedYear = new Date($scope.options.defaultDate).getFullYear();
        $scope.selectedMonth = MONTHS[new Date($scope.options.defaultDate).getMonth()];
        buildCalendar();
    }

    angular.module("flexcalendar", []).directive("flexCalendar", calendarDirective);
}();
