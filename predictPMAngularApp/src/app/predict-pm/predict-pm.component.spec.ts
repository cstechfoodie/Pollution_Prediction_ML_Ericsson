import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictPmComponent } from './predict-pm.component';

describe('PredictPmComponent', () => {
  let component: PredictPmComponent;
  let fixture: ComponentFixture<PredictPmComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PredictPmComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictPmComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
