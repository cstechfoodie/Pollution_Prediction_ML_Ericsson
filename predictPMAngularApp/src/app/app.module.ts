import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PredictPmComponent } from './predict-pm/predict-pm.component';
import { FundamentalNgxModule } from 'fundamental-ngx';

@NgModule({
  declarations: [AppComponent, PredictPmComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FundamentalNgxModule
  ],
  providers: [HttpClientModule],
  bootstrap: [AppComponent]
})
export class AppModule {}
