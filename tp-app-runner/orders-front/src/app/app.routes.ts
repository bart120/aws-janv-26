import { Routes } from '@angular/router';
import { OrdersListComponent } from './pages/orders-list/orders-list.component';
import { OrderDetailComponent } from './pages/order-detail/order-detail.component';

export const routes: Routes = [
    { path: '', redirectTo: 'orders', pathMatch: 'full' },
    { path: 'orders', component: OrdersListComponent },
    { path: 'orders/:id', component: OrderDetailComponent }
];
