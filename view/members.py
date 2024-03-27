from flask import Blueprint, render_template, request, url_for, current_app, redirect
from models import Members, db

members_bp = Blueprint('member', __name__)

@members_bp.route('/register', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email_id = request.form['email_id']
        mobile_no = request.form['mobile_no']
        memberShip_id = request.form['memberShip_id']
        
        #checkbok in html gives a string so for boolean handling it manually i.e (string to boolean)
        isMember = 'isMember' in request.form

        with current_app.app_context():
            mem = Members(name=name, email_id=email_id, mobile_no=mobile_no, isMember=isMember, memberShip_id=memberShip_id)
            db.session.add(mem)
            db.session.commit()
        return redirect(url_for('member.create'))
    return render_template('memberHTML/createMember.html')

@members_bp.route('/updateMember', methods=['GET','POST'])
def updateMember():

    if request.method == 'POST':
        if 'member_id' in request.form:  
            member_id = request.form['member_id']
        
            members = Members.query.get(member_id) 

            if members:
                if 'name' in request.form:  
                    members.name = request.form['name'] 
                if 'email_id' in request.form:
                    members.email_id = request.form['email_id']
                if 'mobile_no' in request.form:  
                    members.mobile_no = request.form['mobile_no'] 
                if 'memberShip_id' in request.form:  
                    members.memberShip_id = request.form['memberShip_id'] 
                # handling checkbox 
                isMember_old = request.form.get('isMember_old', 'off') == 'on' 
                isMember_new = 'isMember' in request.form
                if isMember_old != isMember_new:
                    members.isMember = not members.isMember
                
                db.session.commit()
            return render_template('memberHTML/updateMember.html', members=members, member_id=member_id)
    return render_template('memberHTML/updateMemRes.html')

@members_bp.route('/deleteMember', methods=['GET','POST'])
def deleteMember():
    if request.method == 'POST':
        member_id = request.form['member_id']
        del_member = Members.query.get_or_404(member_id)

        db.session.delete(del_member) 
        db.session.commit()
        return redirect(url_for('member.view'))
    return render_template('memberHTML/updateMemRes.html')

@members_bp.route('/viewMember')
def view():
    all_members = Members.query.all()
    return render_template('/memberHTML/viewMember.html', all_members=all_members)