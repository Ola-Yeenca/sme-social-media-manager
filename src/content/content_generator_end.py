            calendar.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_of_week": current_date.strftime("%A"),
                "theme": theme,
                "english_content": english_content,
                "spanish_content": spanish_content,
                "posting_times": ["09:00", "13:00", "17:00"]  # Suggested posting times
            })
        
        return calendar
