import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Order } from '../models/order';

@Injectable({ providedIn: 'root' })
export class OrdersService {
  private baseUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) { }

  list(): Observable<Order[]> {
    return this.http.get<any>(this.baseUrl).pipe(
      map(response => response.items as Order[])
    );
  }

  getById(id: string): Observable<Order> {
    return this.http.get<Order>(`${this.baseUrl}/${id}`);
  }
}