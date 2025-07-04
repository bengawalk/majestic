import { Route } from './Route';

export class Platform {
  platformNumber: string;
  color: string;
  routes: Route[];

  constructor({
    platformNumber,
    color = '#FFFFFF',
    routes = []
  }: {
    platformNumber: string;
    color?: string;
    routes?: Route[];
  }) {
    this.platformNumber = platformNumber;
    this.color = color;
    this.routes = routes;
  }

  addRoute(route: Route) {
    this.routes.push(route);
  }

  displayName() {
    return `Platform ${this.platformNumber}`;
  }
} 