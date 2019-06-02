import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { PredictPmComponent } from './predict-pm/predict-pm.component';

const routes: Routes = [
  {
    path: 'predict',
    component: PredictPmComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
