# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, BOOLEAN, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, NCHAR, String, Table, Unicode, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class parameter(Base):
    __tablename__ = '_parameter'

    parameter = Column(String(100), primary_key=True)
    value = Column(String(100))


class aos_code(Base):
    __tablename__ = 'aos_code'

    aos_code = Column(CHAR(6), primary_key=True)
    description = Column(String(50))
    fee_cat_id = Column(String(20))
    department_id = Column(NCHAR(3))
    pathway = Column(String(50))
    valid_for_projection = Column(BOOLEAN())
    require_foundation = Column(BOOLEAN())


t_audit_cgroup = Table(
    'audit_cgroup', metadata,
    Column('cgroup_id', Integer, nullable=False),
    Column('description', String(200), nullable=False),
    Column('strand', String(5), nullable=False),
    Column('notes', String(200)),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_component = Table(
    'audit_component', metadata,
    Column('component_id', Integer),
    Column('description', Unicode(200)),
    Column('module_code', String(9)),
    Column('calendar_type', Unicode(20)),
    Column('coordination_eligible', BOOLEAN),
    Column('hecos', Integer),
    Column('staffing_band', Integer),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_cost = Table(
    'audit_cost', metadata,
    Column('cost_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('room_type', String(20)),
    Column('cost_type', String(20), nullable=False),
    Column('description', String(200), nullable=False),
    Column('max_group_size', Integer, nullable=False),
    Column('mins_per_group', Integer, nullable=False),
    Column('cost_per_group', Integer, nullable=False),
    Column('notes', String(8000)),
    Column('number_of_staff', DECIMAL(5, 2)),
    Column('tt_type', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_course = Table(
    'audit_course', metadata,
    Column('course_id', Integer, nullable=False),
    Column('aos_code', CHAR(6)),
    Column('pathway', String(50), nullable=False),
    Column('combined_with', String(50)),
    Column('award', String(10)),
    Column('notes', String(8000)),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_course_session = Table(
    'audit_course_session', metadata,
    Column('course_session_id', Integer, nullable=False),
    Column('session', Integer, nullable=False),
    Column('costc', CHAR(6)),
    Column('description', String(100), nullable=False),
    Column('notes', Unicode),
    Column('curriculum_id', Integer),
    Column('datestamp', DateTime, nullable=False),
    Column('cmd', String(23), nullable=False)
)


t_audit_relationships = Table(
    'audit_relationships', metadata,
    Column('tbl', String(50), nullable=False),
    Column('lcom_username', String(50), nullable=False),
    Column('cmd', String(20), nullable=False),
    Column('datestamp', DateTime, nullable=False),
    Column('parent', Integer, nullable=False),
    Column('child', Integer, nullable=False)
)


class Calendar(Base):
    __tablename__ = 'calendar'

    calendar_type = Column(Unicode(20), primary_key=True)
    long_description = Column(Unicode(200), nullable=False)
    epoch_name = Column(Unicode(20))


class CgroupStrand(Base):
    __tablename__ = 'cgroup_strand'

    strand_id = Column(String(5), primary_key=True)
    description = Column(String(30), nullable=False)


class ComponentStaffing(Base):
    __tablename__ = 'component_staffing'

    band_id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)
    multiplier = Column(DECIMAL(10, 5), nullable=False)


class CostType(Base):
    __tablename__ = 'cost_type'

    cost_type = Column(String(20), primary_key=True)
    cost_multiplier = Column(Float(53), nullable=False,
                             server_default=text("((1))"))
    is_pay = Column(BOOLEAN(), nullable=False)
    is_contact = Column(BOOLEAN(), nullable=False)
    nominal_account = Column(Integer, nullable=False)
    is_assessing = Column(BOOLEAN())
    is_assignment = Column(BOOLEAN())
    is_taught = Column(BOOLEAN())


class CostTypePay(Base):
    __tablename__ = 'cost_type_pay'

    is_pay = Column(BOOLEAN(), primary_key=True)
    description = Column(String(30), nullable=False)


class Costc(Base):
    __tablename__ = 'costc'

    costc = Column(CHAR(6), primary_key=True)
    description = Column(String(50), nullable=False)
    department = Column(String(50))
    pathway = Column(BOOLEAN(), nullable=False)
    primary_aos_code = Column(CHAR(6))
    directorate_id = Column(CHAR(1))


class CurriculumBp(Base):
    __tablename__ = 'curriculum_bp'

    lock = Column(CHAR(1), nullable=False,
                  unique=True, server_default=text("('Z')"))
    curriculum_id = Column(Integer, primary_key=True)


class Department(Base):
    __tablename__ = 'department'

    department_id = Column(NCHAR(3), primary_key=True)
    description = Column(String(50), nullable=False)
    long_description = Column(
        String(50), nullable=False)


class FeeCategory(Base):
    __tablename__ = 'fee_category'

    fee_cat_id = Column(String(20), primary_key=True)
    description = Column(NCHAR(10), nullable=False)


class FeeStatus(Base):
    __tablename__ = 'fee_status'

    fee_status_id = Column(String(20), primary_key=True)
    status_description = Column(
        String(50), nullable=False)
    home_overseas = Column(CHAR(1), nullable=False)


class HecosCode(Base):
    __tablename__ = 'hecos_code'

    hecos = Column(Integer, primary_key=True)
    code_name = Column(String(100), nullable=False)


class Module(Base):
    __tablename__ = 'module'

    module_code = Column(String(9), primary_key=True)
    credits = Column(Integer)
    description = Column(String(100))


class RoomType(Base):
    __tablename__ = 'room_type'

    room_type = Column(String(20), primary_key=True)
    average_sq_metre = Column(Integer, server_default=text("(NULL)"))
    on_campus = Column(BOOLEAN())


class SNOriginConfig(Base):
    __tablename__ = 'student_number_origin_config'

    origin = Column(String(50),
                    primary_key=True, nullable=False)
    set_cat_id = Column(CHAR(3),
                        primary_key=True, nullable=False)


class SNUsage(Base):
    __tablename__ = 'student_number_usage'

    usage_id = Column(String(20), primary_key=True)
    description = Column(String(200))
    surpress_all = Column(BOOLEAN(), server_default=text("((0))"))
    set_cat_id = Column(CHAR(3))


class Audit(Base):
    __tablename__ = 'tt_audit'

    username = Column(String(100), nullable=False)
    datestamp = Column(DateTime, nullable=False)
    action = Column(String(50), nullable=False)
    cost_id = Column(Integer)
    group_id = Column(Integer)
    staff_id = Column(String(50))
    student_id = Column(CHAR(11))
    actioned = Column(BOOLEAN(), server_default=text("((0))"))
    audit_id = Column(Integer, primary_key=True)


class AuditAction(Base):
    __tablename__ = 'tt_audit_action'

    action = Column(String(50), primary_key=True)
    detail_level = Column(String(50), nullable=False)


class Change(Base):
    __tablename__ = 'tt_change'

    tt_change_id = Column(Integer, primary_key=True)
    date_created = Column(Date, nullable=False)
    category = Column(String(50), nullable=False)
    screen = Column(String(50))
    requested_by = Column(String(100))
    description = Column(
        String(8000), nullable=False)
    progress = Column(String(8000))
    closed = Column(BOOLEAN(), nullable=False, server_default=text("((0))"))
    closed_date = Column(Date)
    closed_version = Column(NCHAR(10))
    suspend = Column(BOOLEAN(), server_default=text("((0))"))


class Instrument(Base):
    __tablename__ = 'tt_instrument'

    instrument = Column(String(50), primary_key=True)
    short_instrument = Column(String(50))


class Stage(Base):
    __tablename__ = 'tt_stage'

    stage = Column(String(50), primary_key=True)
    is_pending = Column(BOOLEAN(), nullable=False)


ql_student = Table(
    'tt_student', metadata,
    Column('student_id', CHAR(11), nullable=False),
    Column('name', String(100), nullable=False),
    Column('instrument', String(50))
)


ql_student_enrols = Table(
    'tt_student_enrols', metadata,
    Column('student_id', CHAR(11), nullable=False),
    Column('aos_code', CHAR(6), nullable=False),
    Column('session', Integer, nullable=False),
    Column('acad_year', Integer, nullable=False),
    Column('score', String(10)),
    Column('stage', String(50), nullable=False),
    Column('module_code', String(15), nullable=False)
)


class tt_Type(Base):
    __tablename__ = 'tt_type'

    tt_type_id = Column(Integer, primary_key=True)
    description = Column(String(20), nullable=False)


class Week(Base):
    __tablename__ = 'week'

    celcat_week = Column(Integer, primary_key=True)
    period = Column(Integer, nullable=False)


class CourseSession(Base):
    __tablename__ = 'course_session'

    course_session_id = Column(Integer, primary_key=True)
    session = Column(Integer, nullable=False, server_default=text("((1))"))
    costc = Column(ForeignKey('costc.costc'))
    description = Column(String(100), nullable=False)
    notes = Column(Unicode, server_default=text("(NULL)"))
    curriculum_id = Column(Integer)


class Curriculum(Base):
    __tablename__ = 'curriculum'
    __table_args__ = (
        Index('IX_curriculum', 'acad_year', 'usage_id'),
    )

    curriculum_id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)
    created_date = Column(DateTime, nullable=False)
    acad_year = Column(Integer, nullable=False)
    usage_id = Column(ForeignKey('student_number_usage.usage_id'))
    can_edit = Column(BOOLEAN(), server_default=text("((1))"))


class Course(Base):
    __tablename__ = "course"

    course_id = Column(Integer, primary_key=True)
    aos_code = Column(ForeignKey("aos_code.aos_code"))
    pathway = Column(String(50), nullable=False)
    combined_with = Column(String(50))
    award = Column(String(10))
    curriculum_id = Column(ForeignKey("curriculum.curriculum_id"))

    def __repr__(self):
        return f"{self.course_id}-{self.pathway}: from curriculum {self.curriculum_id}"


class Fee(Base):
    __tablename__ = 'fee'

    acad_year = Column(Integer, primary_key=True, nullable=False)
    fee_cat_id = Column(ForeignKey('fee_category.fee_cat_id'),
                        primary_key=True, nullable=False)
    fee_status_id = Column(ForeignKey(
        'fee_status.fee_status_id'), primary_key=True, nullable=False)
    session = Column(Integer, primary_key=True, nullable=False)
    gross_fee = Column(DECIMAL(10, 2), nullable=False)
    waiver = Column(DECIMAL(10, 2))


class SNInstance(Base):
    __tablename__ = 'student_number_instance'

    instance_id = Column(Integer, primary_key=True)
    acad_year = Column(Integer, nullable=False)
    usage_id = Column(ForeignKey(
        'student_number_usage.usage_id'), nullable=False)
    input_datetime = Column(DateTime, server_default=text("(getdate())"))
    lcom_username = Column(String(50))
    surpress = Column(BOOLEAN(), nullable=False, server_default=text("((0))"))
    costc = Column(ForeignKey('costc.costc'))


class CalendarMap(Base):
    __tablename__ = 'calendar_map'

    acad_week = Column(Integer, primary_key=True, nullable=False)
    curriculum_id = Column(ForeignKey(
        'curriculum.curriculum_id'), primary_key=True, nullable=False)
    term = Column(Integer, nullable=False)
    description = Column(Unicode(50))
    calendar_type = Column(ForeignKey(
        'calendar.calendar_type'), primary_key=True, nullable=False)
    celcat_week = Column(ForeignKey('week.celcat_week'), nullable=False)


class CGroup(Base):
    __tablename__ = 'cgroup'

    cgroup_id = Column(Integer, primary_key=True)
    description = Column(String(200), nullable=False)
    strand = Column(ForeignKey('cgroup_strand.strand_id'),
                    nullable=False, server_default=text("('MISC')"))
    notes = Column(String(8000))
    curriculum_id = Column(ForeignKey('curriculum.curriculum_id'))


class Component(Base):
    __tablename__ = 'component'

    component_id = Column(Integer, primary_key=True)
    description = Column(Unicode(200), nullable=False)
    module_code = Column(String(9))
    calendar_type = Column(ForeignKey('calendar.calendar_type'), nullable=False)
    coordination_eligible = Column(BOOLEAN(), nullable=False)
    hecos = Column(ForeignKey('hecos_code.hecos'))
    staffing_band = Column(Integer)
    curriculum_id = Column(ForeignKey('curriculum.curriculum_id'))


class SN(Base):
    __tablename__ = 'student_number'

    instance_id = Column(ForeignKey(
        'student_number_instance.instance_id'), primary_key=True, nullable=False)
    fee_status_id = Column(ForeignKey(
        'fee_status.fee_status_id'), primary_key=True, nullable=False)
    origin = Column(String(50),
                    primary_key=True, nullable=False)
    aos_code = Column(ForeignKey('aos_code.aos_code'),
                      primary_key=True, nullable=False)
    session = Column(Integer, primary_key=True, nullable=False)
    student_count = Column(DECIMAL(10, 5), nullable=False)


class CGroupConfig(Base):
    __tablename__ = 'cgroup_config'

    cgroup_id = Column(ForeignKey('cgroup.cgroup_id'),
                       primary_key=True, nullable=False, index=True)
    component_id = Column(ForeignKey('component.component_id'),
                          primary_key=True, nullable=False)
    ratio = Column(Integer, nullable=False, server_default=text("((1))"))


class Cost(Base):
    __tablename__ = 'cost'

    cost_id = Column(Integer, primary_key=True)
    component_id = Column(ForeignKey('component.component_id'), nullable=False)
    room_type = Column(ForeignKey('room_type.room_type'))
    cost_type = Column(ForeignKey('cost_type.cost_type'), nullable=False)
    description = Column(String(200), nullable=False)
    max_group_size = Column(Integer, nullable=False)
    mins_per_group = Column(Integer, nullable=False)
    cost_per_group = Column(Integer, nullable=False)
    notes = Column(String(8000))
    number_of_staff = Column(DECIMAL(5, 2))
    tt_type = Column(Integer, server_default=text("((1))"))


class CostWeek(Base):
    __tablename__ = 'cost_week'

    cost_id = Column(ForeignKey('cost.cost_id'),
                     primary_key=True, nullable=False)
    acad_week = Column(Integer, primary_key=True, nullable=False)


class TGroup(Base):
    __tablename__ = 'tt_tgroup'

    tgroup_id = Column(Integer, primary_key=True)
    cost_id = Column(ForeignKey('cost.cost_id'), nullable=False)
    notes = Column(String(255))
    room_type = Column(String(20), nullable=False)


class TGroupMember(Base):
    __tablename__ = 'tt_tgroup_membership'

    tgroup_id = Column(ForeignKey('tt_tgroup.tgroup_id'),
                       primary_key=True, nullable=False)
    student_id = Column(CHAR(11),
                        primary_key=True, nullable=False)


class TGroupStaffing(Base):
    __tablename__ = 'tt_tgroup_staffing'

    tgroup_id = Column(ForeignKey('tt_tgroup.tgroup_id'),
                       primary_key=True, nullable=False)
    staff_id = Column(String(50),
                      primary_key=True, nullable=False)


class CourseConfig(Base):
    __tablename__ = 'course_config'
    course_id = Column(Integer(), ForeignKey('course.course_id'),
                       primary_key=True, nullable=False)
    course_session_id = Column(Integer(), ForeignKey('course_session.course_session_id'),
                               primary_key=True, nullable=False)


class CourseSessionConfig(Base):
    __tablename__ = 'course_session_config'
    course_session_id = Column(Integer(), ForeignKey('course_session.course_session_id'),
                               primary_key=True, nullable=False)
    cgroup_id = Column(Integer(), ForeignKey('cgroup.cgroup_id'),
                       primary_key=True, nullable=False)
