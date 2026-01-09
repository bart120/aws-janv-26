import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-order-detail',
  template: `<h2>Order Detail</h2>`,
  standalone: true,
  imports: [CommonModule]
})
export class OrderDetailComponent { }
