#!/usr/bin/env python3
# center_focused_weather_analyzer.py
# Daily analysis organized by detention center for legal documentation

import json
import datetime
import hashlib
import os
from collections import defaultdict

def load_analysis_data(date_str):
    """Load the existing enhanced analysis data"""
    
    # Try to find the analysis file
    possible_paths = [
        f"daily_analysis/enhanced_analysis_{date_str}.json",
        f"../daily_analysis/enhanced_analysis_{date_str}.json",
        f"enhanced_analysis_{date_str}.json"
    ]
    
    analysis_file = None
    for path in possible_paths:
        if os.path.exists(path):
            analysis_file = path
            break
    
    if not analysis_file:
        print(f"Error: Could not find enhanced analysis file for {date_str}")
        return None
    
    with open(analysis_file, 'r') as f:
        return json.load(f)

def organize_by_detention_center(analysis_data):
    """Organize all hazards and measurements by detention center"""
    
    detailed_analysis = analysis_data['detailed_analysis']
    
    # Group by detention center
    centers = defaultdict(list)
    
    for record in detailed_analysis:
        center_name = record['location']
        centers[center_name].append(record)
    
    return centers

def analyze_center_hazards(center_records):
    """Analyze hazards for a specific detention center throughout the day"""
    
    # Sort records by timestamp to see progression through day
    sorted_records = sorted(center_records, 
                          key=lambda x: x.get('analysis_timestamp', ''))
    
    # Track hazards throughout the day
    hazard_timeline = []
    hazard_summary = defaultdict(int)
    total_hazards = 0
    
    # Track continuous vs intermittent hazards
    hazard_periods = defaultdict(list)
    current_hazards = set()
    
    for i, record in enumerate(sorted_records):
        timestamp = record.get('analysis_timestamp', '')
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
            hour = dt.hour
        except:
            hour = i  # fallback to record order
        
        record_hazards = set()
        
        for hazard in record.get('hazard_analysis', []):
            hazard_type = hazard['type']
            hazard_summary[hazard_type] += 1
            total_hazards += 1
            record_hazards.add(hazard_type)
            
            # Track hazard timeline
            hazard_timeline.append({
                'hour': hour,
                'type': hazard_type,
                'severity': hazard['severity'],
                'description': hazard['description'],
                'measurement': hazard.get('measurement'),
                'risk_level': hazard.get('risk_level'),
                'timestamp': timestamp
            })
        
        # Track continuous periods
        for hazard_type in record_hazards:
            if hazard_type not in current_hazards:
                # New hazard period starting
                hazard_periods[hazard_type].append({
                    'start_hour': hour,
                    'end_hour': hour,
                    'duration': 1
                })
            else:
                # Extend current period
                if hazard_periods[hazard_type]:
                    hazard_periods[hazard_type][-1]['end_hour'] = hour
                    hazard_periods[hazard_type][-1]['duration'] = hour - hazard_periods[hazard_type][-1]['start_hour'] + 1
        
        # Check for hazards that ended
        for hazard_type in current_hazards - record_hazards:
            # Hazard ended, finalize the period
            pass
        
        current_hazards = record_hazards
    
    # Calculate hazard statistics
    unique_hazard_types = len(hazard_summary)
    most_frequent_hazard = max(hazard_summary.items(), key=lambda x: x[1]) if hazard_summary else None
    
    # Get key measurements throughout day
    measurements = {
        'max_heat_index': None,
        'min_heat_index': None,
        'max_temperature': None,
        'min_temperature': None,
        'max_humidity': None,
        'max_precipitation': None,
        'alerts_detected': []
    }
    
    for record in sorted_records:
        raw = record.get('raw_measurements', {})
        
        # Track temperature and heat index ranges
        if raw.get('heat_index_f'):
            hi = raw['heat_index_f']
            if measurements['max_heat_index'] is None or hi > measurements['max_heat_index']:
                measurements['max_heat_index'] = hi
            if measurements['min_heat_index'] is None or hi < measurements['min_heat_index']:
                measurements['min_heat_index'] = hi
        
        if raw.get('temperature_f'):
            temp = raw['temperature_f']
            if measurements['max_temperature'] is None or temp > measurements['max_temperature']:
                measurements['max_temperature'] = temp
            if measurements['min_temperature'] is None or temp < measurements['min_temperature']:
                measurements['min_temperature'] = temp
        
        if raw.get('humidity_percent'):
            humidity = raw['humidity_percent']
            if measurements['max_humidity'] is None or humidity > measurements['max_humidity']:
                measurements['max_humidity'] = humidity
        
        if raw.get('precipitation_rate_in_hr'):
            precip = raw['precipitation_rate_in_hr']
            if measurements['max_precipitation'] is None or precip > measurements['max_precipitation']:
                measurements['max_precipitation'] = precip
        
        # Collect weather alerts
        for hazard in record.get('hazard_analysis', []):
            if hazard['type'] == 'weather_alert':
                alert_text = hazard.get('measurement', '')
                if alert_text and alert_text not in measurements['alerts_detected']:
                    measurements['alerts_detected'].append(alert_text)
    
    return {
        'total_records': len(sorted_records),
        'total_hazards': total_hazards,
        'unique_hazard_types': unique_hazard_types,
        'hazard_summary': dict(hazard_summary),
        'most_frequent_hazard': most_frequent_hazard,
        'hazard_timeline': hazard_timeline,
        'hazard_periods': dict(hazard_periods),
        'measurements': measurements,
        'hours_covered': len(set(h['hour'] for h in hazard_timeline)) if hazard_timeline else 0
    }

def create_center_focused_report(date_str, analysis_data):
    """Create a detention center-focused report"""
    
    centers_data = organize_by_detention_center(analysis_data)
    
    report = {
        'date': date_str,
        'analysis_timestamp': datetime.datetime.now().isoformat(),
        'total_centers': len(centers_data),
        'centers': {}
    }
    
    # Analyze each center
    for center_name, records in centers_data.items():
        center_analysis = analyze_center_hazards(records)
        report['centers'][center_name] = center_analysis
    
    return report

def print_center_focused_summary(report):
    """Print a detention center-focused summary"""
    
    print(f"\nDETENTION CENTER WEATHER ANALYSIS - {report['date']}")
    print("=" * 80)
    print(f"Total Centers Analyzed: {report['total_centers']}")
    print(f"Analysis Timestamp: {report['analysis_timestamp']}")
    
    # Sort centers by total hazards (most concerning first)
    sorted_centers = sorted(report['centers'].items(), 
                          key=lambda x: x[1]['total_hazards'], 
                          reverse=True)
    
    for center_name, center_data in sorted_centers:
        print(f"\n{'='*60}")
        print(f"📍 {center_name.upper()}")
        print(f"{'='*60}")
        
        print(f"Total Hazard Detections: {center_data['total_hazards']}")
        print(f"Hours of Data: {center_data['hours_covered']}/24")
        print(f"Unique Hazard Types: {center_data['unique_hazard_types']}")
        
        if center_data['most_frequent_hazard']:
            hazard_type, count = center_data['most_frequent_hazard']
            print(f"Most Frequent Hazard: {hazard_type.replace('_', ' ').title()} ({count} times)")
        
        # Key measurements
        measurements = center_data['measurements']
        print(f"\nKEY MEASUREMENTS:")
        if measurements['max_heat_index']:
            print(f"  Heat Index Range: {measurements['min_heat_index']:.1f}°F - {measurements['max_heat_index']:.1f}°F")
        if measurements['max_temperature']:
            print(f"  Temperature Range: {measurements['min_temperature']:.1f}°F - {measurements['max_temperature']:.1f}°F")
        if measurements['max_humidity']:
            print(f"  Maximum Humidity: {measurements['max_humidity']:.1f}%")
        if measurements['max_precipitation']:
            print(f"  Maximum Precipitation: {measurements['max_precipitation']:.2f} in/hr")
        
        # Hazard breakdown
        if center_data['hazard_summary']:
            print(f"\nHAZARD BREAKDOWN:")
            for hazard_type, count in center_data['hazard_summary'].items():
                hazard_display = hazard_type.replace('_', ' ').title()
                if hazard_type == 'heat_index_risk':
                    hazard_display = "Heat Index Risk"
                elif hazard_type == 'precipitation_flood_risk':
                    hazard_display = "Flood Risk"
                print(f"  • {hazard_display}: {count} detections")
        
        # Weather alerts
        if measurements['alerts_detected']:
            print(f"\nWEATHER ALERTS:")
            for alert in measurements['alerts_detected']:
                print(f"  • {alert}")
        
        # Hazard timeline (show key periods)
        if center_data['hazard_timeline']:
            print(f"\nHAZARD TIMELINE:")
            
            # Group by hazard type for cleaner display
            timeline_by_type = defaultdict(list)
            for event in center_data['hazard_timeline']:
                timeline_by_type[event['type']].append(event)
            
            for hazard_type, events in timeline_by_type.items():
                hazard_display = hazard_type.replace('_', ' ').title()
                hours = sorted(set(e['hour'] for e in events))
                
                if len(hours) <= 3:
                    hour_display = ', '.join(f"{h:02d}:00" for h in hours)
                else:
                    # Show range for long periods
                    if max(hours) - min(hours) == len(hours) - 1:
                        # Continuous period
                        hour_display = f"{min(hours):02d}:00 - {max(hours):02d}:00 (continuous)"
                    else:
                        # Intermittent
                        hour_display = f"{len(hours)} hours total (intermittent)"
                
                print(f"  • {hazard_display}: {hour_display}")
                
                # Show severity info for first event
                if events:
                    severity = events[0]['severity']
                    risk_level = events[0].get('risk_level', '')
                    if risk_level:
                        print(f"    Risk Level: {risk_level} | Severity: {severity}")

def save_center_focused_report(date_str, report):
    """Save the center-focused report"""
    
    # Create directory for center reports
    base_dir = os.path.dirname(os.getcwd()) if os.path.basename(os.getcwd()) == 'Scripts' else os.getcwd()
    reports_dir = os.path.join(base_dir, "center_reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Save JSON version
    json_filename = f"center_analysis_{date_str}.json"
    json_path = os.path.join(reports_dir, json_filename)
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Save human-readable version
    txt_filename = f"center_report_{date_str}.txt"
    txt_path = os.path.join(reports_dir, txt_filename)
    
    with open(txt_path, 'w') as f:
        f.write(f"DETENTION CENTER WEATHER ANALYSIS - {report['date']}\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total Centers Analyzed: {report['total_centers']}\n")
        f.write(f"Analysis Timestamp: {report['analysis_timestamp']}\n\n")
        
        # Sort centers by total hazards
        sorted_centers = sorted(report['centers'].items(), 
                              key=lambda x: x[1]['total_hazards'], 
                              reverse=True)
        
        for center_name, center_data in sorted_centers:
            f.write(f"{'='*60}\n")
            f.write(f"📍 {center_name.upper()}\n")
            f.write(f"{'='*60}\n")
            
            f.write(f"Total Hazard Detections: {center_data['total_hazards']}\n")
            f.write(f"Hours of Data: {center_data['hours_covered']}/24\n")
            f.write(f"Unique Hazard Types: {center_data['unique_hazard_types']}\n")
            
            if center_data['most_frequent_hazard']:
                hazard_type, count = center_data['most_frequent_hazard']
                f.write(f"Most Frequent Hazard: {hazard_type.replace('_', ' ').title()} ({count} times)\n")
            
            # Key measurements
            measurements = center_data['measurements']
            f.write(f"\nKEY MEASUREMENTS:\n")
            if measurements['max_heat_index']:
                f.write(f"  Heat Index Range: {measurements['min_heat_index']:.1f}°F - {measurements['max_heat_index']:.1f}°F\n")
            if measurements['max_temperature']:
                f.write(f"  Temperature Range: {measurements['min_temperature']:.1f}°F - {measurements['max_temperature']:.1f}°F\n")
            if measurements['max_humidity']:
                f.write(f"  Maximum Humidity: {measurements['max_humidity']:.1f}%\n")
            if measurements['max_precipitation']:
                f.write(f"  Maximum Precipitation: {measurements['max_precipitation']:.2f} in/hr\n")
            
            # Hazard breakdown
            if center_data['hazard_summary']:
                f.write(f"\nHAZARD BREAKDOWN:\n")
                for hazard_type, count in center_data['hazard_summary'].items():
                    hazard_display = hazard_type.replace('_', ' ').title()
                    if hazard_type == 'heat_index_risk':
                        hazard_display = "Heat Index Risk"
                    elif hazard_type == 'precipitation_flood_risk':
                        hazard_display = "Flood Risk"
                    f.write(f"  • {hazard_display}: {count} detections\n")
            
            # Weather alerts
            if measurements['alerts_detected']:
                f.write(f"\nWEATHER ALERTS:\n")
                for alert in measurements['alerts_detected']:
                    f.write(f"  • {alert}\n")
            
            f.write(f"\n")
    
    return json_path, txt_path

def main():
    """Main function for center-focused analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create detention center-focused weather analysis')
    parser.add_argument('--date', help='Date to analyze (YYYY-MM-DD)', 
                       default=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
    
    args = parser.parse_args()
    
    print(f"Loading analysis data for {args.date}...")
    
    # Load existing analysis
    analysis_data = load_analysis_data(args.date)
    if not analysis_data:
        return
    
    print(f"Creating center-focused report...")
    
    # Create center-focused report
    report = create_center_focused_report(args.date, analysis_data)
    
    # Save reports
    json_path, txt_path = save_center_focused_report(args.date, report)
    
    # Print summary
    print_center_focused_summary(report)
    
    print(f"\nFILES CREATED:")
    print(f"JSON Report: {json_path}")
    print(f"Text Report: {txt_path}")
    
    # Quick summary for next steps
    total_hazards = sum(center['total_hazards'] for center in report['centers'].values())
    print(f"\nQUICK SUMMARY:")
    print(f"• {total_hazards} total hazard detections across {len(report['centers'])} centers")
    print(f"• Each 'hazard detection' = one hazard type found in one hourly reading")
    print(f"• Use the detailed timeline above to see when hazards occurred")
    print(f"• Next: We can add time range analysis (specific hours) and hazard duration tracking")

if __name__ == "__main__":
    main()
