import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Component({
  selector: 'app-predict-pm',
  templateUrl: './predict-pm.component.html',
  styleUrls: ['./predict-pm.component.scss']
})
export class PredictPmComponent implements OnInit {
  predictedPm: string = 'WhyNotDisplayThisString';
  testCondition: string =
    '2848.0,2010.0,1.0,15.0,19.0,91.0,-15.0,-6.0,1037.0,cv,1.78,0.0,0.0';
  changed: boolean = false;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    console.log(this.http);

    this.http
      .get<string>('http://localhost:9090/predict')
      .pipe(catchError((error: any) => throwError(error.json())))
      .subscribe(res => (this.predictedPm = res));
  }

  tryAnother() {
    this.http
      .post<string>('http://localhost:9090/predict', this.testCondition)
      .pipe(catchError((error: any) => throwError(error.json())))
      .subscribe(res => {
        if (res !== this.predictedPm) {
          this.changed = true;
        } else {
          this.changed = false;
        }
        this.predictedPm = res;
      });
  }
}
