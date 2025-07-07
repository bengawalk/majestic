import type { Area } from './Area';
import type { Stop } from './Stop';

export interface Route {
  number: string;
  area: Area;
  stops: Stop[];
  via: Area;
  destination: string;
  kannadaDestination?: string;
  platformNumber: string;
  // Add other fields as needed
}

export class Route {
  number: string;
  area: Area;
  via: Area;
  stops: Stop[];
  destination: string;
  kannadaDestination?: string;
  platformNumber: string;

  constructor({
    number,
    area,
    stops,
    via,
    destination,
    kannadaDestination,
    platformNumber
  }: {
    number: string;
    area: Area;
    stops: Stop[];
    via: Area;
    destination: string;
    kannadaDestination?: string;
    platformNumber: string;
  }) {
    this.number = number;
    this.area = area;
    this.stops = stops;
    this.via = via;
    this.destination = destination;
    this.kannadaDestination = kannadaDestination;
    this.platformNumber = platformNumber;
  }

  // displayName() {
  //   return `${this.number} → ${this.destination} via ${this.via.name}`;
  // }
} 