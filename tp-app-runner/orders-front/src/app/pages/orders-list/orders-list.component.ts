import { Component, OnInit } from '@angular/core';
import { OrdersService } from '../../services/orders.service';
import { Order } from '../../models/order';

@Component({
  selector: 'app-orders-list',
  template: `<h2>Orders</h2><ul><li *ngFor="let o of orders">{{ o.id }}</li></ul>`
})
export class OrdersListComponent implements OnInit {
  orders: Order[] = [];
  constructor(private service: OrdersService) {}
  ngOnInit() {
    this.service.list().subscribe(data => this.orders = data);
  }
}