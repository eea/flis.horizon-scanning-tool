DOC_TREND_TYPE_CHOICES = (
    (1, 'Trend'),
    (2, 'Megatrend'),
)

DOC_UNCERTAINTIES_TYPE_CHOICES = (
    (1, 'Rationale'),
    (2, 'Data'),
    (3, 'Methodology (related to the model)'),
)

DOC_TIME_HORIZON_CHOICES = (
    (1, '1 year'),
    (5, '5 years'),
    (10, '10 years'),
    (50, '50 years'),
    (100, '100 years'),
    (200, 'more than 100 years'),
)

RELATION_TYPE_CHOICES = (
    (1, 'Cause-effect relationship'),
    (2, 'Neutral relationship'),
)

CANONICAL_ROLES = (
    'Authenticated',
    'Administrator',
    'Contributor',
    'Viewer',
    'Reviewer',
)

IMPACT_TYPES = (
    ('risk', 'Risk'),
    ('opportunity', 'Opportunity'),
    ('other', 'Other'),
)
