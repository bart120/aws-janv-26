import { Component, OnInit, signal, Signal } from '@angular/core';
import { OrdersService } from '../../services/orders.service';
import { Order } from '../../models/order';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-orders-list',
  template: `<h2>Orders, table Dynamo</h2><ul><li *ngFor="let o of orders()">{{ o.order_id }} - {{ o.amount }} {{ o.currency }}</li></ul>`,
  standalone: true,
  imports: [CommonModule]
})
export class OrdersListComponent implements OnInit {
  orders = signal<Order[]>([]);
  constructor(private service: OrdersService) { }
  ngOnInit() {
    this.service.list().subscribe(data => this.orders.set(data));
  }
}