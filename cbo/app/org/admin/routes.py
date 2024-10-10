# CBO Financial Overview
@admin_bp.route('/cbo_summary')
@login_required
def cbo_summary():
    total_amount = Contribution.query.with_entities(db.func.sum(Contribution.amount)).scalar() or 0
    total_fines = Fine.query.with_entities(db.func.sum(Fine.amount)).scalar() or 0
    members = Member.query.all()
    
    member_financials = {}
    for member in members:
        contributions = Contribution.query.filter_by(member_id=member.id).all()
        fines = Fine.query.filter_by(member_id=member.id).all()
        
        total_contributions = sum(contribution.amount for contribution in contributions)
        total_fines = sum(fine.amount for fine in fines)
        balance = total_contributions - total_fines
        
        member_financials[member.id] = {
            'name': member.name,
            'total_contributions': total_contributions,
            'total_fines': total_fines,
            'balance': balance,
        }

    return render_template('admin/cbo_summary.html', member_financials=member_financials, total_amount=total_amount)



@admin_bp.route('/attendance_summary')
@login_required
def attendance_summary():
    members = Member.query.all()
    attendance_summary = {}
    total_meetings = Meeting.query.count()  # Total meetings held

    for member in members:
        attendance_records = Attendance.query.filter_by(member_id=member.id).all()
        total_attended = sum(1 for record in attendance_records if record.status == 'Present')
        total_absent = sum(1 for record in attendance_records if record.status == 'Absent')
        total_late = sum(1 for record in attendance_records if record.status == 'Late')
        
        attendance_summary[member.id] = {
            'name': member.name,
            'total_attended': total_attended,
            'total_absent': total_absent,
            'total_late': total_late,
            'attendance_percentage': (total_attended / total_meetings * 100) if total_meetings > 0 else 0,
        }

    return render_template('admin/attendance_summary.html', attendance_summary=attendance_summary)






